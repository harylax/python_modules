#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  lambda_spells.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: haryandr <haryandr@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/03 12:37:15 by haryandr        #+#    #+#               #
#  Updated: 2026/07/06 15:27:13 by haryandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any


def artifact_sorter(artifacts: list[dict[Any, Any]]) -> list[dict[Any, Any]]:
    return sorted(
        artifacts, key=lambda artifact: artifact['power'], reverse=True
        )


def power_filter(
        mages: list[dict[Any, Any]],
        min_power: int) -> list[dict[Any, Any]]:
    return list(filter(lambda mage: mage['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict[Any, Any]]) -> dict[Any, Any]:
    return {
        'max_power': max(mages, key=lambda mage: mage['power'])['power'],
        'min_power': min(mages, key=lambda mage: mage['power'])['power'],
        'avg_power': round(sum(map(
            lambda mage: mage['power'], mages
            )) / len(mages), 2)
    }


if __name__ == "__main__":
    artifacts = [
        {'name': 'Crystal Orb', 'power': 75, 'type': 'weapon'},
        {'name': 'Wind Cloak', 'power': 80, 'type': 'relic'},
        {'name': 'Water Chalice', 'power': 112, 'type': 'accessory'},
        {'name': 'Lightning Rod', 'power': 83, 'type': 'focus'}
        ]
    mages = [
        {'name': 'Alex', 'power': 87, 'element': 'lightning'},
        {'name': 'Storm', 'power': 100, 'element': 'lightning'},
        {'name': 'Riley', 'power': 91, 'element': 'shadow'},
        {'name': 'Zara', 'power': 67, 'element': 'shadow'},
        {'name': 'River', 'power': 64, 'element': 'wind'}
        ]
    spells = ['tsunami', 'shield', 'flash', 'darkness']

    print("\nTesting artifact sorter...")
    sorted_artifacts: list[dict[Any, Any]] = artifact_sorter(artifacts)
    for i in range(1, len(sorted_artifacts)):
        before = sorted_artifacts[i - 1]
        after = sorted_artifacts[i]
        print(
            f"{before['name']} ({before['power']} power) "
            f"comes before {after['name']} ({after['power']} power)"
            )

    print("\nTesting power filter...")
    min_power: int = 70
    print(f"Mages with power greater or equal to {min_power}:")
    filtered_mages: list[dict[Any, Any]] = power_filter(mages, min_power)
    for mage in filtered_mages:
        print(mage)

    print("\nTesting spell transformer...")
    print(spell_transformer(spells))

    print("\nTesting mage stats...")
    print(mage_stats(mages))
