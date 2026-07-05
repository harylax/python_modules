def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    # tmp = artifacts
    # new = []

    # def find_min(artifacts: list[dict]) -> dict:
    #     min_ = artifacts[0]
    #     for i in range(len(artifacts)):
    #         if min_['power'] > artifacts[i]['power']:
    #             min_ = artifacts[i]
    #     return min_
    # while tmp:
    #     min_ = find_min(tmp)
    #     new.append(tmp.pop(tmp.index(min_)))
    # return new
    return sorted(artifacts, key=lambda artifact: artifact['power'])


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    # return [mage for mage in mages if mage['power'] >= min_power]
    return list(filter(lambda mage: mage['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    # new = []
    # for spell in spells:
    #     new.append(f"*{spell}*")
    # return new
    return list(map(lambda spell: f"*{spell}*", spells))


def mage_stats(mages: list[dict]) -> dict:
    return {
        'max_power': max(map(lambda mage: mage['power'], mages)),
        'min_power': min(map(lambda mage: mage['power'], mages)),
        'avg_power': sum(map(lambda mage: mage['power'], mages)) / len(mages)
        }


if __name__ == "__main__":
    artifacts = [
        {'name': 'Storm Crown', 'power': 108, 'type': 'accessory'},
        {'name': 'Fire Staff', 'power': 81, 'type': 'accessory'},
        {'name': 'Light Prism', 'power': 78, 'type': 'accessory'},
        {'name': 'Earth Shield', 'power': 82, 'type': 'armor'}
        ]
    mages = [
        {'name': 'Casey', 'power': 76, 'element': 'shadow'},
        {'name': 'Ash', 'power': 69, 'element': 'light'},
        {'name': 'Casey', 'power': 50, 'element': 'ice'},
        {'name': 'Morgan', 'power': 100, 'element': 'lightning'},
        {'name': 'Ember', 'power': 77, 'element': 'water'}
        ]
    spells = ['shield', 'flash', 'fireball', 'heal']

    print("\nartifact_sorter:")
    print(artifact_sorter(artifacts))

    print("\npower_filter:")
    print(power_filter(mages, 75))

    print("\nspell_transformer:")
    print(spell_transformer(spells))

    print("\nmage_stats:")
    print(mage_stats(mages))
