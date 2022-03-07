BASE    = data/cooking
FILE    = $(BASE)/cooking.stackexchange.txt
PREPROC = cooking.preprocessed.txt

TESTNUM   = 3000
TRAIN     = cooking.train
TEST      = cooking.test
SCRIPT    = script.sh
MODELBASE = model_cooking
MODEL     = $(MODELBASE).bin

.PHONY:	default all clean test try
default:
	@echo 'Try the following targets:'
	@echo '  all:    Create all files.'
	@echo '  clean:  Clean generated files.'
	@echo '  test:   Run the tests.'
	@echo '  test5:  Run the tests with top 5 instead of 1.'
	@echo '  try:    Try running on manual input.'

all:	$(TRAIN) $(TEST) $(MODEL)

clean:
	rm -f -- "$(PREPROC)" "$(TRAIN)" "$(TEST)" "$(MODELBASE)"*

try:	$(MODEL)
	echo 'Trying (CTRL-D when done) ...'
	fasttext predict "$(MODEL)" -

test:	$(MODEL) $(TEST)
	fasttext test "$(MODEL)" "$(TEST)"

test5:	$(MODEL) $(TEST)
	fasttext test "$(MODEL)" "$(TEST)" 5

$(PREPROC):	$(FILE)
	# Separate punctuation, and convert to lowercase.
	cat -- "$(<)" \
		| sed -e "s/\([.\!?,'/()]\)/ \1 /g" \
		| tr '[:upper:]' '[:lower:]' \
		>"$@"

# Use -$(TESTNUM) so that all but the last TESTNUM are used for training.
# The last $(TESTNUM) will be used for testing.
$(TRAIN):	$(PREPROC)
	head -n "-$(TESTNUM)" -- "$<" >"$@"

$(TEST):	$(PREPROC)
	tail -n "$(TESTNUM)" -- "$<" >"$@"

$(MODEL):	$(SCRIPT) $(TRAIN)
	./script.sh "$(TRAIN)" "$(MODELBASE)"
