#!/usr/bin/env python3
#
# Copyright (c) 2022, Michael Shafae
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
#

"""Example of how to use us_state.pckl and ca_county.pckl pickle files."""

from collections import namedtuple
import pickle
import locale

State = namedtuple(
    'State',
    [
        'name',
        'area_sq_mi',
        'land_area_sq_mi',
        'water_area_sq_mi',
        'population',
        'n_rep_votes',
        'n_senate_votes',
        'n_ec_votes',
    ],
)

CACounty = namedtuple(
    'CACounty', ['name', 'county_seat', 'population', 'area_sq_mi']
)


def _str(item):
    """Handy function to return the named field name of a state or county."""
    return f'{item.name}'


State.__str__ = _str
CACounty.__str__ = _str


def main():
    """Main function"""
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    with open('ca_county.pckl', 'rb') as file_handle:
        ca_counties = pickle.load(file_handle)

    with open('us_state.pckl', 'rb') as file_handle:
        states = pickle.load(file_handle)

    states.sort(key=lambda x: x.area_sq_mi)
    print(
        f'The largest state or territory by area is {states[-1]} ' \
        f'and the smallest one is {states[0]}.'
    )

    ca_counties.sort(key=lambda x: x.area_sq_mi)
    print(
        f'The largest CA county by area is {ca_counties[-1]}'
        f' and the smallest one is {ca_counties[0]}.'
    )

    total_us_population = sum([s.population for s in states])
    print(f'The total US population is {total_us_population:n}.')
    # territories_only = [s for s in states if s.n_ec_votes == 0]
    states_only = [s for s in states if s.n_ec_votes > 0]
    print(f"The states are {states_only[0]}")
    total_states_only_population = sum([s.population for s in states_only])
    print(
        f'The total US population from states is {total_states_only_population:n}.'
    )
    total_states_boundary_ec_votes = sum([s.n_ec_votes for s in states_only if (37,956,694 < s.population < 41,119,752)])
    
    print(f"The total EC votes for those states within that boundary is {total_states_boundary_ec_votes:n}")
    ec_votes_cali = [s.n_ec_votes for s in states_only if s.name == "California"]
    ec_votes_cali = ec_votes_cali[0]
    sub_ec_votes = total_states_boundary_ec_votes - ec_votes_cali
    print(f"California has {ec_votes_cali} electoral votes.")
    print(f"The difference between the boundary states' and California's electoral votes is {sub_ec_votes}")
    print(
        'This means that there are '
        f'{total_us_population - total_states_only_population:n} people'
        ' who live in US territories.'
    )
    total_ec_votes = sum([s.n_ec_votes for s in states])
    print(f'The total number of Electoral College votes is {total_ec_votes}.')

    total_ca_population = sum([c.population for c in ca_counties])
    print(f'The total population of California is {total_ca_population:n}.')
    print(
        'California is '
        f'{(total_ca_population / total_us_population) * 100:.2f}% of '
        ' the US total population.'
    )
    ca_counties.sort(key=lambda x: x.population, reverse=True)
    n_counties = 3
    ca_population_largest_counties = sum(
        [c.population for c in ca_counties[:n_counties]]
    )
    county_names = ', '.join(map(str, ca_counties[:n_counties]))
    print(
        f'The population of the largest {n_counties} counties '
        f'({county_names}) in CA is {ca_population_largest_counties:n} '
        'which is '
        f'{(ca_population_largest_counties / total_ca_population) * 100:.2f}%'
        ' of CA total population or '
        f'{(ca_population_largest_counties / total_us_population) * 100:.2f}%'
        ' of the US population.'
    )

if __name__ == '__main__':
    main()
