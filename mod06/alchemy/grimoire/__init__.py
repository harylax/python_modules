from .light_spellbook import light_spell_record
# from .dark_spellbook import dark_spell_record
# Ne pas exposer dark_spell_record ici
# pour eviter le circular import se declencher ici
# --> crash du kaboom_0 aussi si non


__all__ = ["light_spell_record"]
