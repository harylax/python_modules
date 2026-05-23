if __name__ == "__main__":
    print("=== Kaboom 1 ===")
    print("Access to alchemy/grimoire/dark_spellbook.py directly")
    print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    print("Testing record dark spell: ", end="")
    from alchemy.grimoire.red_spell_record import red_spell_record
    print((
        red_spell_record('Fantasy', 'Earth, wind and fire')
        ))
