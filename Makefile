BABELBIN     = pybabel
PROJECT_NAME = secualert
PACKAGE_DIR  = sphinxcontrib/$(PROJECT_NAME)
LOCALE_DIR   = $(PACKAGE_DIR)/locale
POT          = $(LOCALE_DIR)/$(PROJECT_NAME).pot

# Put it first so that "make" without argument is like "make help".
help:
	@echo "Makefile usage:"
	@echo "    make [target1 [target2 [...]]]"
	@echo ""
	@echo "Available targets:"
	@echo "    help: Default target, printing this help message."
	@echo "    pot: Generate new version of i18n POT catalog template."
	@echo "    po: Update message catalogs from POT file."
	@echo "    mo: Compile message catalogs in MO files."
	@echo ""

.PHONY: help pot

pot:
	@$(BABELBIN) extract --output=$(POT) "$(PACKAGE_DIR)"

po:
	@$(BABELBIN) update --input-file=$(POT) --domain=$(PROJECT_NAME) --output-dir=$(LOCALE_DIR)

mo:
	@$(BABELBIN) compile --directory=$(LOCALE_DIR) --domain=$(PROJECT_NAME)

