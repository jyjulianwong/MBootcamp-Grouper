import json
from typing import Dict, List, Optional, Tuple
from itertools import combinations, permutations
from models import consts


class Grouper:
    def __init__(self, data: Optional[Dict] = None):
        self.data = {}
        if data:
            self.data = data
        else:
            try:
                with open('MBootcamp-2022-Data.json') as sample_data:
                    self.data = json.load(sample_data)
            except:
                pass

        self.group_count = 0

        self.sop = []
        self.alt = []
        self.ten = []
        self.bas = []
        self.vp = []
        self.new = []
        self.old = []

        self.min_count_violation_stat = 0
        self.same_group_violation_stat = 0
        self.diff_group_violation_stat = 0

    def _get_perms(self, people: List[str], group_count: int) -> Tuple:
        min_per_group = len(people) // group_count
        print(f"Grouper: _get_perms: min_per_group: {min_per_group}")
        extra_count = len(people) % group_count
        print(f"Grouper: _get_perms: extra_count: {extra_count}")
        base_assignment = []
        for c in range(group_count):
            for i in range(min_per_group):
                base_assignment.append(c)
        print(f"Grouper: _get_perms: base_assignment: {base_assignment}")
        # 11 3
        # min_per_group = 3
        # extra_count = 2
        # 1 2 3 + 1 2
        # 1 2 3 + 1 3
        # 1 2 3 + 2 3
        extra_assignments = []
        if extra_count:
            extra_assignments = \
                list(map(list, combinations(base_assignment, extra_count)))
        print(f"Grouper: _get_perms: extra_assignments: {extra_assignments}")

        assignments = []
        if len(extra_assignments) != 0:
            for extra_assignment in extra_assignments:
                assignments.append(base_assignment + extra_assignment)
        else:
            assignments.append(base_assignment)

        perms_perms = [permutations(a) for a in assignments]
        perms_tuple = [list(p) for p in perms_perms]
        perms_tuple = sum(perms_tuple, [])
        perms_tuple = [tuple(p) for p in perms_tuple]
        print(f"Grouper: _get_perms: perms_tuple: {perms_tuple}")
        perms_tuple = tuple(set(perms_tuple))
        print(f"Grouper: _get_perms: perms_tuple: {perms_tuple}")
        print(f"Grouper: _get_perms: len(perms_tuple): {len(perms_tuple)}")
        return perms_tuple

    def _valid_combo(self, combo: Dict[str, int]) -> bool:
        for constraint in self.data['constraints']:
            if constraint['type'] == consts.MIN_COUNT:
                member_type = constraint['args'][0]
                min_count = constraint['args'][1]

                members_in_type = []
                if member_type == consts.NEW_MEMBER:
                    members_in_type = self.new
                if member_type == consts.OLD_MEMBER:
                    members_in_type = self.old
                if len(members_in_type) == 0:
                    raise ValueError('Grouper: _valid_combo: Bad constraint')

                for curr_group in range(self.group_count):
                    count = 0
                    for name, group in combo.items():
                        if group != curr_group:
                            continue
                        if name in members_in_type:
                            count += 1

                    if count < min_count:
                        self.min_count_violation_stat += 1
                        return False

            if constraint['type'] == consts.SAME_GROUP:
                name_1 = constraint['args'][0]
                name_2 = constraint['args'][1]
                if combo[name_1] != combo[name_2]:
                    self.same_group_violation_stat += 1
                    return False

            if constraint['type'] == consts.DIFF_GROUP:
                name_1 = constraint['args'][0]
                name_2 = constraint['args'][1]
                if combo[name_1] == combo[name_2]:
                    self.diff_group_violation_stat += 1
                    return False

        return True

    def get_groups(self) -> Tuple[List[List[List[str]]], str]:
        if self.data is None or len(self.data.items()) == 0:
            return [], "No data was supplied."

        self.group_count = self.data['groupCount']
        print(f"Grouper: get_groups: group_count: {self.group_count}")

        for member in self.data['people']:
            for voice in member['voices']:
                if voice == consts.SOP:
                    self.sop.append(member['name'])
                if voice == consts.ALT:
                    self.alt.append(member['name'])
                if voice == consts.TEN:
                    self.ten.append(member['name'])
                if voice == consts.BAS:
                    self.bas.append(member['name'])
                if voice == consts.VP:
                    self.vp.append(member['name'])
            if member['newMember']:
                self.new.append(member['name'])
            else:
                self.old.append(member['name'])

        print(f'Grouper: get_groups: self.sop: {self.sop}')
        print(f'Grouper: get_groups: self.alt: {self.alt}')
        print(f'Grouper: get_groups: self.ten: {self.ten}')
        print(f'Grouper: get_groups: self.bas: {self.bas}')
        print(f'Grouper: get_groups: self.new: {self.new}')
        print(f'Grouper: get_groups: self.old: {self.old}')

        min_group_count = \
            min(map(lambda x: len(x), [self.sop, self.alt, self.ten, self.bas]))
        if self.group_count < min_group_count:
            raise ValueError('Grouper: get_groups: group_count is too small')

        combos = []

        sop_mem_perms = self._get_perms(self.sop, self.group_count)
        print(f"Grouper: get_groups: sop_mem_perms: {sop_mem_perms}")
        alt_mem_perms = self._get_perms(self.alt, self.group_count)
        print(f"Grouper: get_groups: alt_mem_perms: {alt_mem_perms}")
        ten_mem_perms = self._get_perms(self.ten, self.group_count)
        print(f"Grouper: get_groups: ten_mem_perms: {ten_mem_perms}")
        bas_mem_perms = self._get_perms(self.bas, self.group_count)
        print(f"Grouper: get_groups: bas_mem_perms: {bas_mem_perms}")

        for sop_mem_perm in sop_mem_perms:
            for alt_mem_perm in alt_mem_perms:
                for ten_mem_perm in ten_mem_perms:
                    for bas_mem_perm in bas_mem_perms:
                        combo = {}

                        for i in range(len(self.sop)):
                            combo[self.sop[i]] = sop_mem_perm[i]
                        for i in range(len(self.alt)):
                            combo[self.alt[i]] = alt_mem_perm[i]
                        for i in range(len(self.ten)):
                            combo[self.ten[i]] = ten_mem_perm[i]
                        for i in range(len(self.bas)):
                            combo[self.bas[i]] = bas_mem_perm[i]

                        combos.append(combo)

        print(f"{len(combos)} combinations generated. Scanning...")

        valid_combos = [combo for combo in combos if self._valid_combo(combo)]

        result = []
        for valid_combo_count in range(len(valid_combos)):
            print(f"VALID COMBO {valid_combo_count + 1}")
            combo = valid_combos[valid_combo_count]
            combo_groups = []

            for group in range(self.group_count):
                group_members = []

                for member, member_group in combo.items():
                    if member_group == group:
                        group_members.append(member)

                combo_groups.append(group_members)
                print(f"Group {group + 1}: {group_members}")

            result.append(combo_groups)
            print("\n")

        statistics = ""
        statistics += f"Grouper: get_groups: self.group_count: {self.group_count}"
        statistics += f"Grouper: get_groups: Possible combinations: {len(combos)}"
        statistics += f"Grouper: get_groups: Valid combinations: {len(valid_combos)}"

        return result, statistics
