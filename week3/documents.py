#
# A simple endpoint that can receive documents from an external source, mark them up and return them.  This can be useful
# for hooking in callback functions during indexing to do smarter things like classification
#
from flask import (
    Blueprint, request, abort, current_app, jsonify
)
import fasttext
import json

bp = Blueprint('documents', __name__, url_prefix='/documents')

# Take in a JSON document and return a JSON document
@bp.route('/annotate', methods=['POST'])
def annotate():
    if request.mimetype == 'application/json':
        the_doc = request.get_json()
        response = {}
        cat_model = current_app.config.get("cat_model", None) # see if we have a category model
        syns_model = current_app.config.get("syns_model", None) # see if we have a synonyms/analogies model
        name_transformer = current_app.config.get("transformer", None)
        # We have a map of fields to annotate.  Do POS, NER on each of them
        sku = the_doc["sku"]
        for item in the_doc:
            the_text = the_doc[item]
            if the_text is not None and the_text.find("%{") == -1:
                if item == "name":
                    if syns_model is not None and name_transformer is not None:
                        name_synonyms = set()
                        for token in name_transformer.transform(the_text).split():
                            nearest_neighbors = \
                                syns_model.get_nearest_neighbors(the_text, k=32)
                            for (score, synonym) in nearest_neighbors:
                                if (score > 0.999):
                                    name_synonyms.add(synonym)
                        response["synonyms"] = tuple(name_synonyms)
        return jsonify(response)
    abort(415)
