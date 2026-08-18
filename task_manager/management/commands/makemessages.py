from django.core.management.commands import makemessages


class Command(makemessages.Command):
    # Appends the native gettext flag to drop fuzzy suggestions entirely
    msgmerge_options = makemessages.Command.msgmerge_options + ["--no-fuzzy-matching"]