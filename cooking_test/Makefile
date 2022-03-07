BASE = data/cooking
FILE = $(BASE)/cooking.stackexchange.txt

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
	@echo '  try:    Try running on manual input.'

all:	$(TRAIN) $(TEST) $(MODEL)

clean:
	rm -f -- "$(TRAIN)" "$(TEST)" "$(MODELBASE)"*

try:	$(MODEL)
	echo 'Trying (CTRL-D when done) ...'
	fasttext predict "$(MODEL)" -

test:	$(MODEL) $(TEST)
	fasttext test "$(MODEL)" "$(TEST)"

# Use -$(TESTNUM) so that all but the last TESTNUM are used for training.
# The last $(TESTNUM) will be used for testing.
$(TRAIN):
	head -n "-$(TESTNUM)" -- "$(FILE)" >"$@"

$(TEST):
	tail -n "$(TESTNUM)" -- "$(FILE)" >"$@"

$(MODEL):	$(SCRIPT) $(TRAIN)
	./script.sh "$(TRAIN)" "$(MODELBASE)"
