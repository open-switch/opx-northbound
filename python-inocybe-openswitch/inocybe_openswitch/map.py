#!/usr/bin/env python
# Copyright (c) 2018 Inocybe Technologies.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT
# LIMITATION ANY IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS
# FOR A PARTICULAR PURPOSE, MERCHANTABLITY OR NON-INFRINGEMENT.
#
# See the Apache Version 2.0 License for specific language governing
# permissions and limitations under the License.


'''Mapping of CPS operations onto JSON RPC'''

import re

class TypeMap(object):
    '''Perform type mappings for cases where CPS does not do
       it correctly
    '''
    def __init__(self, init_map):
        self.the_map = init_map

    def add(self, key, parsers):
        '''Add a parser to map. Parsers are a tupple of in/out'''
        self.the_map[key] = parsers

    def delete(self, key):
        '''Remove a parser to a map'''
        del self.the_map[key]

    def to_cps(self, key, data):
        '''Convert to cps'''
        try:
            (to_cps, from_cps) = self.the_map[key]
            return to_cps(data)
        except KeyError:
            return data

    def from_cps(self, key, data):
        '''Convert to cps'''
        try:
            (to_cps, from_cps) = self.the_map[key]
            return from_cps(data)
        except KeyError:
            return data

def _bool_to_cps(data):
    '''Convert boolean to archaic C (modern C has bool)'''
    if data:
        return 1
    else:
        return 0

def _bool_from_cps(data):
    '''Convert boolean to archaic C (modern C has bool)'''
    return data != 0

def _strip_module_to_cps(data):
    '''Convert boolean to archaic C (modern C has bool)'''
    return data

MODULE_RE = re.compile(".*:")

def _strip_module_from_cps(data):
    '''Convert boolean to archaic C (modern C has bool)'''
    return MODULE_RE.sub("", data)

FIX_IF_TYPE_RE = re.compile("iana-if-type:")
REV_FIX_IF_TYPE_RE = re.compile("ianaift:")

def _fix_iftype_to_cps(data):
    '''Convert boolean to archaic C (modern C has bool)'''
    return FIX_IF_TYPE_RE.sub("ianaift:", data)

def _fix_iftype_from_cps(data):
    '''Convert boolean to archaic C (modern C has bool)'''
    return REV_FIX_IF_TYPE_RE.sub("iana-if-type:", data)


########################################################
#
# EVERYTHING FROM HERE DOWNWARDS SHOULD BECOME GENERATED
#
########################################################

VLAN_MAP = {"MANAGEMENT":2, "DATA":1}
REV_VLAN_MAP = {2:"MANAGEMENT", 1:"DATA"}

def _fix_vlan_type_to_cps(data):
    '''Fix vlan type to CPS'''
    return VLAN_MAP[data]

def _fix_vlan_type_from_cps(data):
    '''Convert vlan type to enum'''
    return REV_VLAN_MAP[data]

DUPLEX_MAP = {"full":1, "half":2, "auto":3}
REV_DUPLEX_MAP = {1:"full", 2:"half", 3:"auto"}

def _fix_duplex_type_to_cps(data):
    '''Fix vlan type to CPS'''
    return DUPLEX_MAP[data]

def _fix_duplex_type_from_cps(data):
    '''Convert vlan type to enum'''
    return REV_DUPLEX_MAP[data]

MODE_MAP = {"MODE_NONE":1, "MODE_L2":2, "MODE_L2HYBRID":3, "MODE_L3":4, "MODE_L2DISABLED":5}
REV_MODE_MAP = {1:"MODE_NONE", 2:"MODE_L2", 3:"MODE_L2HYBRID", 4:"MODE_L3", 5:"MODE_L2DISABLED"}

def _fix_mode_to_cps(data):
    '''Fix vlan type to CPS'''
    return MODE_MAP[data]

def _fix_mode_from_cps(data):
    '''Convert vlan type to enum'''
    return REV_MODE_MAP[data]


SPEED_MAP = {"0MBPS":0, "10MBPS":1, "100MBPS":2, "1GIGE":3, "10GIGE":4,
             "25GIGE":5, "40GIGE":6, "100GIGE":7, "AUTO":8, "20GIGE":9,
             "50GIGE":10, "200GIGE":11, "400GIGE":12, "4GFC":13, "8GFC":14,
             "16GFC":15, "32GFC":16}
REV_SPEED_MAP = {0:"0MBPS", 1:"10MBPS", 2:"100MBPS", 3:"1GIGE", 4:"10GIGE",
                 5:"25GIGE", 6:"40GIGE", 7:"100GIGE", 8:"AUTO", 9:"20GIGE",
                 10:"50GIGE", 11:"200GIGE", 12:"400GIGE", 13:"4GFC", 14:"8GFC",
                 15:"16GFC", 16:"32GFC"}

def _fix_speed_to_cps(data):
    '''Fix ifspeed to CPS'''
    return SPEED_MAP[data]

def _fix_speed_from_cps(data):
    '''Convert ifspeed to enum'''
    return REV_SPEED_MAP[data]

REV_MEDIA_MAP = {1:"AR_POPTICS_NOTPRESENT",
2:"AR_POPTICS_UNKNOWN",
3:"AR_POPTICS_NOTSUPPORTED",
4:"AR_SFPPLUS_10GBASE_USR",
5:"AR_SFPPLUS_10GBASE_SR",
6:"AR_SFPPLUS_10GBASE_LR",
7:"AR_SFPPLUS_10GBASE_ER",
8:"AR_SFPPLUS_10GBASE_ZR",
9:"AR_SFPPLUS_10GBASE_CX4",
10:"AR_SFPPLUS_10GBASE_LRM",
11:"AR_SFPPLUS_10GBASE_T",
12:"AR_SFPPLUS_10GBASE_CUHALFM",
13:"AR_SFPPLUS_10GBASE_CU1M",
14:"AR_SFPPLUS_10GBASE_CU2M",
15:"AR_SFPPLUS_10GBASE_CU3M",
16:"AR_SFPPLUS_10GBASE_CU5M",
17:"AR_SFPPLUS_10GBASE_CU7M",
18:"AR_SFPPLUS_10GBASE_CU10M",
19:"AR_SFPPLUS_10GBASE_ACU7M",
20:"AR_SFPPLUS_10GBASE_ACU10M",
21:"AR_SFPPLUS_10GBASE_ACU15M",
22:"AR_SFPPLUS_10GBASE_DWDM",
23:"AR_SFPPLUS_10GBASE_DWDM_40KM",
24:"AR_SFPPLUS_10GBASE_DWDM_80KM",
25:"AR_QSFP_40GBASE_SR4",
26:"AR_QSFP_40GBASE_SR4_EXT",
27:"AR_QSFP_40GBASE_LR4",
28:"AR_QSFP_40GBASE_LM4",
29:"AR_QSFP_40GBASE_PSM4_LR",
30:"AR_QSFP_40GBASE_PSM4_1490NM",
31:"AR_QSFP_40GBASE_PSM4_1490NM_1M",
32:"AR_QSFP_40GBASE_PSM4_1490NM_3M",
33:"AR_QSFP_40GBASE_PSM4_1490NM_5M",
34:"AR_4x1_1000BASE_T",
35:"AR_QSFP_40GBASE_CR4_HAL_M",
36:"AR_QSFP_40GBASE_CR4_1M",
37:"AR_QSFP_40GBASE_CR4_2M",
38:"AR_QSFP_40GBASE_CR4_3M",
39:"AR_QSFP_40GBASE_CR4_5M",
40:"AR_QSFP_40GBASE_CR4_7M",
41:"AR_QSFP_40GBASE_CR4_10M",
42:"AR_QSFP_40GBASE_CR4_50M",
43:"AR_QSFP_40GBASE_CR4",
44:"AR_4x10_10GBASE_CR1_HAL_M",
45:"AR_4x10_10GBASE_CR1_1M",
46:"AR_4x10_10GBASE_CR1_3M",
47:"AR_4x10_10GBASE_CR1_5M",
48:"AR_4x10_10GBASE_CR1_7M",
49:"AR_SFPPLUS_FC_8GBASE_SR",
50:"AR_SFPPLUS_FC_8GBASE_IR",
51:"AR_SFPPLUS_FC_8GBASE_MR",
52:"AR_SFPPLUS_FC_8GBASE_LR",
53:"SFP_SX",
54:"SFP_LX",
55:"SFP_ZX",
56:"SFP_CX",
57:"SFP_DX",
58:"SFP_T",
59:"SFP_FX",
60:"SFP_CWDM",
61:"SFP_IR1",
62:"SFP_LR1",
63:"SFP_LR2",
64:"SFP_BX10",
65:"SFP_PX",
66:"4x_10GBASE_SR_AOCXXM",
67:"QSFP_40GBASE_SM4",
68:"QSFP_40GBASE_ER4",
69:"QSFP_4x10_10GBASE_CR1_2M",
70:"SFPPLUS_10GBASE_ZR_TUNABLE",
71:"AR_QSFP28_100GBASE_SR4",
72:"AR_QSFP28_100GBASE_LR4",
73:"AR_QSFP28_100GBASE_CWDM4",
74:"AR_QSFP28_100GBASE_PSM4_IR",
75:"AR_QSFP28_100GBASE_CR4",
76:"AR_QSFP28_100GBASE_AOC",
77:"AR_QSFP28_100GBASE_CR4_HAL_M",
78:"AR_QSFP28_100GBASE_CR4_1M",
79:"AR_QSFP28_100GBASE_CR4_2M",
80:"AR_QSFP28_100GBASE_CR4_3M",
81:"AR_QSFP28_100GBASE_CR4_4M",
82:"AR_QSFP28_100GBASE_CR4_5M",
83:"QSFP28_100GBASE_CR4_7M",
84:"QSFP28_100GBASE_CR4_10M",
85:"QSFP28_100GBASE_CR4_50M",
86:"4X25_25GBASE_CR1_HALF_M",
87:"4X25_25GBASE_CR1_1M",
88:"4X25_25GBASE_CR1_2M",
89:"4X25_25GBASE_CR1_3M",
90:"4X25_25GBASE_CR1_4M",
91:"4X25_25GBASE_CR1",
92:"2X50_50GBASE_CR2_HALF_M",
93:"2X50_50GBASE_CR2_1M",
94:"2X50_50GBASE_CR2_2M",
95:"2X50_50GBASE_CR2_3M",
96:"2X50_50GBASE_CR2_4M",
97:"2X50_50GBASE_CR2",
98:"SFP28_25GBASE_CR1",
99:"SFP28_25GBASE_CR1_HALF_M",
100:"SFP28_25GBASE_CR1_1M",
101:"SFP28_25GBASE_CR1_2M",
102:"SFP28_25GBASE_CR1_3M",
103:"QSFPPLUS_50GBASE_CR2",
104:"QSFPPLUS_50GBASE_CR2_1M",
105:"QSFPPLUS_50GBASE_CR2_2M",
106:"QSFPPLUS_50GBASE_CR2_3M",
107:"QSFP_40GBASE_BIDI",
108:"QSFP_40GBASE_AOC",
109:"QSFP28_100GBASE_LR4_LITE",
110:"QSFP28_100GBASE_ER4",
111:"QSFP28_100GBASE_ACC",
112:"SFP28_25GBASE_SR",
113:"SFPPLUS_10GBASE_SR_AOCXXM",
114:"SFP_BX10_UP",
115:"SFP_BX10_DOWN",
116:"SFP_BX40_UP",
117:"SFP_BX40_DOWN",
118:"SFP_BX80_UP",
119:"SFP_BX80_DOWN",
120:"QSFP28_100GBASE_PSM4_PIGTAIL",
121:"QSFP28_100GBASE_SWDM4",
122:"QSFP_40GBASE_PSM4_PIGTAIL",
123:"AR_QSFP_40GBASE_CR4_HALFM",
124:"AR_4x10_10GBASE_CR1_HALFM",
125:"AR_QSFP28_100GBASE_CR4_HALFM",
126:"4X25_25GBASE_CR1_HALFM",
127:"2X50_50GBASE_CR2_HALFM",
128:"SFP28_25GBASE_CR1_HALFM",
129:"SFPPLUS_8GBASE_FC_SW",
130:"SFPPLUS_8GBASE_FC_LW",
131:"SFPPLUS_16GBASE_FC_SW",
132:"SFPPLUS_16GBASE_FC_LW",
133:"QSFPPLUS_64GBASE_FC_SW4",
134:"QSFPPLUS_4X16_16GBASE_FC_SW",
135:"QSFPPLUS_64GBASE_FC_LW4",
136:"QSFPPLUS_4X16_16GBASE_FC_LW",
137:"QSFP28_128GBASE_FC_SW4",
138:"QSFP28_4X32_32GBASE_FC_SW",
139:"QSFP28_128GBASE_FC_LW4",
140:"QSFP28_4X32_32GBASE_FC_LW",
141:"SFP28_32GBASE_FC_SW",
142:"SFP28_32GBASE_FC_LW",
143:"SFP28_25GBASE_SR_NOF",
144:"SFP28_25GBASE_eSR",
145:"SFP28_25GBASE_LR",
146:"SFP28_25GBASE_LR_LITE",
147:"SFP28_25GBASE_SR_AOCXXM",
148:"SFP28_25GBASE_CR1_LPBK",
149:"QSFP28-DD_200GBASE_CR4_HALFM",
150:"QSFP28-DD_200GBASE_CR4_1M",
151:"QSFP28-DD_200GBASE_CR4_2M",
152:"QSFP28-DD_200GBASE_CR4_3M",
153:"QSFP28-DD_200GBASE_CR4_5M",
154:"QSFP28-DD_200GBASE_CR4",
155:"QSFP28-DD_200GBASE_CR4_1_HALFM",
156:"QSFP28-DD_200GBASE_CR4_2_HALFM",
157:"QSFP28-DD_2x100GBASE_CR4_1M",
158:"QSFP28-DD_2x100GBASE_CR4_2M",
159:"QSFP28-DD_2x100GBASE_CR4_3M",
160:"QSFP28-DD_8x25GBASE_CR4_1M",
161:"QSFP28-DD_8x25GBASE_CR4_2M",
162:"QSFP28-DD_8x25GBASE_CR4_3M",
163:"QSFP28-DD_200GBASE_CR4_LPBK",
164:"SFPPLUS_10GBASE_CR_1_HALFM",
165:"SFPPLUS_10GBASE_CR_2_HALFM",
166:"SFPPLUS_10GBASE_CR_1M",
167:"SFPPLUS_10GBASE_CR_2M",
168:"SFPPLUS_10GBASE_CR_3M",
169:"SFPPLUS_10GBASE_CR_4M",
170:"SFPPLUS_10GBASE_CR_5M",
171:"QSFP28-DD_200GBASE_SR4_HALFM",
172:"QSFP28-DD_200GBASE_SR4_1M",
173:"QSFP28-DD_200GBASE_SR4_2M",
174:"QSFP28-DD_200GBASE_SR4_3M",
175:"QSFP28-DD_200GBASE_SR4_5M",
176:"QSFP28-DD_200GBASE_SR4",
177:"QSFP28-DD_200GBASE_SR4_1_HALFM",
178:"QSFP28-DD_200GBASE_SR4_2_HALFM",
179:"1GBASE_COPPER",
180:"10GBASE_COPPER",
181:"25GBASE_BACKPLANE",
182:"SFPPLUS_10GBASE_SR_AOC1M",
183:"SFPPLUS_10GBASE_SR_AOC3M",
184:"SFPPLUS_10GBASE_SR_AOC5M",
185:"SFPPLUS_10GBASE_SR_AOC10M",
186:"QSFPPLUS_4X10_10GBASE_SR_AOC10M",
187:"QSFPPLUS_40GBASE_SR_AOC3M",
188:"QSFPPLUS_40GBASE_SR_AOC5M",
189:"QSFPPLUS_40GBASE_SR_AOC7M",
190:"QSFPPLUS_40GBASE_SR_AOC10M",
}
OUT_MEDIA_MAP = {"AR_POPTICS_NOTPRESENT":1,
"AR_POPTICS_UNKNOWN":2,
"AR_POPTICS_NOTSUPPORTED":3,
"AR_SFPPLUS_10GBASE_USR":4,
"AR_SFPPLUS_10GBASE_SR":5,
"AR_SFPPLUS_10GBASE_LR":6,
"AR_SFPPLUS_10GBASE_ER":7,
"AR_SFPPLUS_10GBASE_ZR":8,
"AR_SFPPLUS_10GBASE_CX4":9,
"AR_SFPPLUS_10GBASE_LRM":10,
"AR_SFPPLUS_10GBASE_T":11,
"AR_SFPPLUS_10GBASE_CUHALFM":12,
"AR_SFPPLUS_10GBASE_CU1M":13,
"AR_SFPPLUS_10GBASE_CU2M":14,
"AR_SFPPLUS_10GBASE_CU3M":15,
"AR_SFPPLUS_10GBASE_CU5M":16,
"AR_SFPPLUS_10GBASE_CU7M":17,
"AR_SFPPLUS_10GBASE_CU10M":18,
"AR_SFPPLUS_10GBASE_ACU7M":19,
"AR_SFPPLUS_10GBASE_ACU10M":20,
"AR_SFPPLUS_10GBASE_ACU15M":21,
"AR_SFPPLUS_10GBASE_DWDM":22,
"AR_SFPPLUS_10GBASE_DWDM_40KM":23,
"AR_SFPPLUS_10GBASE_DWDM_80KM":24,
"AR_QSFP_40GBASE_SR4":25,
"AR_QSFP_40GBASE_SR4_EXT":26,
"AR_QSFP_40GBASE_LR4":27,
"AR_QSFP_40GBASE_LM4":28,
"AR_QSFP_40GBASE_PSM4_LR":29,
"AR_QSFP_40GBASE_PSM4_1490NM":30,
"AR_QSFP_40GBASE_PSM4_1490NM_1M":31,
"AR_QSFP_40GBASE_PSM4_1490NM_3M":32,
"AR_QSFP_40GBASE_PSM4_1490NM_5M":33,
"AR_4x1_1000BASE_T":34,
"AR_QSFP_40GBASE_CR4_HAL_M":35,
"AR_QSFP_40GBASE_CR4_1M":36,
"AR_QSFP_40GBASE_CR4_2M":37,
"AR_QSFP_40GBASE_CR4_3M":38,
"AR_QSFP_40GBASE_CR4_5M":39,
"AR_QSFP_40GBASE_CR4_7M":40,
"AR_QSFP_40GBASE_CR4_10M":41,
"AR_QSFP_40GBASE_CR4_50M":42,
"AR_QSFP_40GBASE_CR4":43,
"AR_4x10_10GBASE_CR1_HAL_M":44,
"AR_4x10_10GBASE_CR1_1M":45,
"AR_4x10_10GBASE_CR1_3M":46,
"AR_4x10_10GBASE_CR1_5M":47,
"AR_4x10_10GBASE_CR1_7M":48,
"AR_SFPPLUS_FC_8GBASE_SR":49,
"AR_SFPPLUS_FC_8GBASE_IR":50,
"AR_SFPPLUS_FC_8GBASE_MR":51,
"AR_SFPPLUS_FC_8GBASE_LR":52,
"SFP_SX":53,
"SFP_LX":54,
"SFP_ZX":55,
"SFP_CX":56,
"SFP_DX":57,
"SFP_T":58,
"SFP_FX":59,
"SFP_CWDM":60,
"SFP_IR1":61,
"SFP_LR1":62,
"SFP_LR2":63,
"SFP_BX10":64,
"SFP_PX":65,
"4x_10GBASE_SR_AOCXXM":66,
"QSFP_40GBASE_SM4":67,
"QSFP_40GBASE_ER4":68,
"QSFP_4x10_10GBASE_CR1_2M":69,
"SFPPLUS_10GBASE_ZR_TUNABLE":70,
"AR_QSFP28_100GBASE_SR4":71,
"AR_QSFP28_100GBASE_LR4":72,
"AR_QSFP28_100GBASE_CWDM4":73,
"AR_QSFP28_100GBASE_PSM4_IR":74,
"AR_QSFP28_100GBASE_CR4":75,
"AR_QSFP28_100GBASE_AOC":76,
"AR_QSFP28_100GBASE_CR4_HAL_M":77,
"AR_QSFP28_100GBASE_CR4_1M":78,
"AR_QSFP28_100GBASE_CR4_2M":79,
"AR_QSFP28_100GBASE_CR4_3M":80,
"AR_QSFP28_100GBASE_CR4_4M":81,
"AR_QSFP28_100GBASE_CR4_5M":82,
"QSFP28_100GBASE_CR4_7M":83,
"QSFP28_100GBASE_CR4_10M":84,
"QSFP28_100GBASE_CR4_50M":85,
"4X25_25GBASE_CR1_HALF_M":86,
"4X25_25GBASE_CR1_1M":87,
"4X25_25GBASE_CR1_2M":88,
"4X25_25GBASE_CR1_3M":89,
"4X25_25GBASE_CR1_4M":90,
"4X25_25GBASE_CR1":91,
"2X50_50GBASE_CR2_HALF_M":92,
"2X50_50GBASE_CR2_1M":93,
"2X50_50GBASE_CR2_2M":94,
"2X50_50GBASE_CR2_3M":95,
"2X50_50GBASE_CR2_4M":96,
"2X50_50GBASE_CR2":97,
"SFP28_25GBASE_CR1":98,
"SFP28_25GBASE_CR1_HALF_M":99,
"SFP28_25GBASE_CR1_1M":100,
"SFP28_25GBASE_CR1_2M":101,
"SFP28_25GBASE_CR1_3M":102,
"QSFPPLUS_50GBASE_CR2":103,
"QSFPPLUS_50GBASE_CR2_1M":104,
"QSFPPLUS_50GBASE_CR2_2M":105,
"QSFPPLUS_50GBASE_CR2_3M":106,
"QSFP_40GBASE_BIDI":107,
"QSFP_40GBASE_AOC":108,
"QSFP28_100GBASE_LR4_LITE":109,
"QSFP28_100GBASE_ER4":110,
"QSFP28_100GBASE_ACC":111,
"SFP28_25GBASE_SR":112,
"SFPPLUS_10GBASE_SR_AOCXXM":113,
"SFP_BX10_UP":114,
"SFP_BX10_DOWN":115,
"SFP_BX40_UP":116,
"SFP_BX40_DOWN":117,
"SFP_BX80_UP":118,
"SFP_BX80_DOWN":119,
"QSFP28_100GBASE_PSM4_PIGTAIL":120,
"QSFP28_100GBASE_SWDM4":121,
"QSFP_40GBASE_PSM4_PIGTAIL":122,
"AR_QSFP_40GBASE_CR4_HALFM":123,
"AR_4x10_10GBASE_CR1_HALFM":124,
"AR_QSFP28_100GBASE_CR4_HALFM":125,
"4X25_25GBASE_CR1_HALFM":126,
"2X50_50GBASE_CR2_HALFM":127,
"SFP28_25GBASE_CR1_HALFM":128,
"SFPPLUS_8GBASE_FC_SW":129,
"SFPPLUS_8GBASE_FC_LW":130,
"SFPPLUS_16GBASE_FC_SW":131,
"SFPPLUS_16GBASE_FC_LW":132,
"QSFPPLUS_64GBASE_FC_SW4":133,
"QSFPPLUS_4X16_16GBASE_FC_SW":134,
"QSFPPLUS_64GBASE_FC_LW4":135,
"QSFPPLUS_4X16_16GBASE_FC_LW":136,
"QSFP28_128GBASE_FC_SW4":137,
"QSFP28_4X32_32GBASE_FC_SW":138,
"QSFP28_128GBASE_FC_LW4":139,
"QSFP28_4X32_32GBASE_FC_LW":140,
"SFP28_32GBASE_FC_SW":141,
"SFP28_32GBASE_FC_LW":142,
"SFP28_25GBASE_SR_NOF":143,
"SFP28_25GBASE_eSR":144,
"SFP28_25GBASE_LR":145,
"SFP28_25GBASE_LR_LITE":146,
"SFP28_25GBASE_SR_AOCXXM":147,
"SFP28_25GBASE_CR1_LPBK":148,
"QSFP28-DD_200GBASE_CR4_HALFM":149,
"QSFP28-DD_200GBASE_CR4_1M":150,
"QSFP28-DD_200GBASE_CR4_2M":151,
"QSFP28-DD_200GBASE_CR4_3M":152,
"QSFP28-DD_200GBASE_CR4_5M":153,
"QSFP28-DD_200GBASE_CR4":154,
"QSFP28-DD_200GBASE_CR4_1_HALFM":155,
"QSFP28-DD_200GBASE_CR4_2_HALFM":156,
"QSFP28-DD_2x100GBASE_CR4_1M":157,
"QSFP28-DD_2x100GBASE_CR4_2M":158,
"QSFP28-DD_2x100GBASE_CR4_3M":159,
"QSFP28-DD_8x25GBASE_CR4_1M":160,
"QSFP28-DD_8x25GBASE_CR4_2M":161,
"QSFP28-DD_8x25GBASE_CR4_3M":162,
"QSFP28-DD_200GBASE_CR4_LPBK":163,
"SFPPLUS_10GBASE_CR_1_HALFM":164,
"SFPPLUS_10GBASE_CR_2_HALFM":165,
"SFPPLUS_10GBASE_CR_1M":166,
"SFPPLUS_10GBASE_CR_2M":167,
"SFPPLUS_10GBASE_CR_3M":168,
"SFPPLUS_10GBASE_CR_4M":169,
"SFPPLUS_10GBASE_CR_5M":170,
"QSFP28-DD_200GBASE_SR4_HALFM":171,
"QSFP28-DD_200GBASE_SR4_1M":172,
"QSFP28-DD_200GBASE_SR4_2M":173,
"QSFP28-DD_200GBASE_SR4_3M":174,
"QSFP28-DD_200GBASE_SR4_5M":175,
"QSFP28-DD_200GBASE_SR4":176,
"QSFP28-DD_200GBASE_SR4_1_HALFM":177,
"QSFP28-DD_200GBASE_SR4_2_HALFM":178,
"1GBASE_COPPER":179,
"10GBASE_COPPER":180,
"25GBASE_BACKPLANE":181,
"SFPPLUS_10GBASE_SR_AOC1M":182,
"SFPPLUS_10GBASE_SR_AOC3M":183,
"SFPPLUS_10GBASE_SR_AOC5M":184,
"SFPPLUS_10GBASE_SR_AOC10M":185,
"QSFPPLUS_4X10_10GBASE_SR_AOC10M":186,
"QSFPPLUS_40GBASE_SR_AOC3M":187,
"QSFPPLUS_40GBASE_SR_AOC5M":188,
"QSFPPLUS_40GBASE_SR_AOC7M":189,
"QSFPPLUS_40GBASE_SR_AOC10M":190,
}

def _fix_media_to_cps(data):
    '''Fix ifspeed to CPS'''
    return OUT_MEDIA_MAP[data]

def _fix_media_from_cps(data):
    '''Convert ifspeed to enum'''
    return REV_MEDIA_MAP[data]

REV_TAGGING_MODE_MAP = {1:"UNTAGGED",
2:"TAGGED",
3:"HYBRID",
}
OUT_TAGGING_MODE_MAP = {"UNTAGGED":1,
"TAGGED":2,
"HYBRID":3,
}
def _fix_tagging_mode_to_cps(data):
    '''Fix ifspeed to CPS'''
    return OUT_TAGGING_MODE_MAP[data]

def _fix_tagging_mode_from_cps(data):
    '''Convert ifspeed to enum'''
    return REV_TAGGING_MODE_MAP[data]

REV_LEARN_MODE_MAP = {1:"DROP",
2:"DISABLE",
3:"HW",
4:"CPU_TRAP",
5:"CPU_LOG",
}
OUT_LEARN_MODE_MAP = {"DROP":1,
"DISABLE":2,
"HW":3,
"CPU_TRAP":4,
"CPU_LOG":5,
}

def _fix_learn_mode_to_cps(data):
    '''Fix ifspeed to CPS'''
    return OUT_LEARN_MODE_MAP[data]

def _fix_learn_mode_from_cps(data):
    '''Convert ifspeed to enum'''
    return REV_LEARN_MODE_MAP[data]

REV_FEC_MAP = {1:"auto",
2:"off",
3:"cl91-rs",
4:"cl74-fc",
5:"cl108-rs",
6:"not-supported",
}
OUT_FEC_MAP = {"auto":1,
"off":2,
"cl91-rs":3,
"cl74-fc":4,
"cl108-rs":5,
"not-supported":6,
}
def _fix_fec_to_cps(data):
    '''Fix ifspeed to CPS'''
    return OUT_FEC_MAP[data]

def _fix_fec_from_cps(data):
    '''Convert ifspeed to enum'''
    return REV_FEC_MAP[data]

REV_BREAKOUT_MODE_MAP = {1:"DISABLED",
2:"BREAKOUT_4x1",
3:"BREAKOUT_2x1",
4:"BREAKOUT_1x1",
5:"BREAKOUT_8x2",
6:"BREAKOUT_2x2",
7:"BREAKOUT_4x4",
8:"BREAKOUT_2x4",
9:"BREAKOUT_4x2",
10:"BREAKOUT_UNKNOWN"
}
OUT_BREAKOUT_MODE_MAP = {"DISABLED":1,
"BREAKOUT_4x1":2,
"BREAKOUT_2x1":3,
"BREAKOUT_1x1":4,
"BREAKOUT_8x2":5,
"BREAKOUT_2x2":6,
"BREAKOUT_4x4":7,
"BREAKOUT_2x4":8,
"BREAKOUT_4x2":9,
"BREAKOUT_UNKNOWN":10
}

def _fix_breakout_mode_to_cps(data):
    '''Fix ifspeed to CPS'''
    return OUT_BREAKOUT_MODE_MAP[data]

def _fix_breakout_mode_from_cps(data):
    '''Convert ifspeed to enum'''
    return REV_BREAKOUT_MODE_MAP[data]

REV_CLEAR_COUNTERS = {1:"ALL",
2:"ALL-ETH",
3:"ALL-LAG",
4:"ALL-VLAN",
5:"ALL-LOOPBACK",
6:"ALL-MGMT",
7:"ALL-FC",
}
OUT_CLEAR_COUNTERS = {"ALL":1,
"ALL-ETH":2,
"ALL-LAG":3,
"ALL-VLAN":4,
"ALL-LOOPBACK":5,
"ALL-MGMT":6,
"ALL-FC":7
}

def _fix_clear_counters_to_cps(data):
    '''Fix ifspeed to CPS'''
    return OUT_CLEAR_COUNTERS[data]

def _fix_clear_counters_from_cps(data):
    '''Convert ifspeed to enum'''
    return REV_CLEAR_COUNTERS[data]

IN_MATCH_TYPE_MAP = {1:"SRC_IPV6", 
2:"DST_IPV6", 
3:"SRC_MAC", 
4:"DST_MAC", 
5:"SRC_IP", 
6:"DST_IP", 
7:"IN_PORTS", 
8:"OUT_PORTS", 
9:"IN_PORT", 
10:"OUT_PORT", 
11:"OUTER_VLAN_ID", 
12:"OUTER_VLAN_PRI", 
13:"OUTER_VLAN_CFI", 
14:"INNER_VLAN_ID", 
15:"INNER_VLAN_PRI", 
16:"INNER_VLAN_CFI", 
17:"L4_SRC_PORT", 
18:"L4_DST_PORT", 
19:"ETHER_TYPE", 
20:"IP_PROTOCOL", 
21:"DSCP", 
22:"TTL", 
23:"TOS", 
24:"IP_FLAGS", 
25:"TCP_FLAGS", 
26:"IP_TYPE", 
27:"IP_FRAG", 
28:"IPV6_FLOW_LABEL", 
29:"TC", 
30:"ECN", 
31:"ICMP_TYPE", 
32:"ICMP_CODE", 
33:"SRC_PORT", 
34:"DST_PORT", 
35:"NEIGHBOR_DST_HIT", 
36:"ROUTE_DST_HIT", 
37:"IN_INTFS", 
38:"OUT_INTFS", 
39:"IN_INTF", 
40:"OUT_INTF", 
41:"SRC_INTF", 
42:"UDF", 
43:"IPV6_NEXT_HEADER", 
44:"RANGE_CHECK", 
45:"FDB_DST_HIT", 
}
OUT_MATCH_TYPE_MAP = {"SRC_IPV6":1,
"DST_IPV6":2,
"SRC_MAC":3,
"DST_MAC":4,
"SRC_IP":5,
"DST_IP":6,
"IN_PORTS":7,
"OUT_PORTS":8,
"IN_PORT":9,
"OUT_PORT":10,
"OUTER_VLAN_ID":11,
"OUTER_VLAN_PRI":12,
"OUTER_VLAN_CFI":13,
"INNER_VLAN_ID":14,
"INNER_VLAN_PRI":15,
"INNER_VLAN_CFI":16,
"L4_SRC_PORT":17,
"L4_DST_PORT":18,
"ETHER_TYPE":19,
"IP_PROTOCOL":20,
"DSCP":21,
"TTL":22,
"TOS":23,
"IP_FLAGS":24,
"TCP_FLAGS":25,
"IP_TYPE":26,
"IP_FRAG":27,
"IPV6_FLOW_LABEL":28,
"TC":29,
"ECN":30,
"ICMP_TYPE":31,
"ICMP_CODE":32,
"SRC_PORT":33,
"DST_PORT":34,
"NEIGHBOR_DST_HIT":35,
"ROUTE_DST_HIT":36,
"IN_INTFS":37,
"OUT_INTFS":38,
"IN_INTF":39,
"OUT_INTF":40,
"SRC_INTF":41,
"UDF":42,
"IPV6_NEXT_HEADER":43,
"RANGE_CHECK":44,
"FDB_DST_HIT":45,
}

def _fix_match_type_to_cps(data):
    '''Fix match type to CPS'''
    return OUT_MATCH_TYPE_MAP[data]

def _fix_match_type_from_cps(data):
    '''Convert match type from CPS'''
    return IN_MATCH_TYPE_MAP[data]

IN_COUNTER_TYPE_MAP = {1:"PACKET", 
2:"BYTE", 
}
OUT_COUNTER_TYPE_MAP = {"PACKET":1,
"BYTE":2,
}

def _fix_counter_type_to_cps(data):
    '''Fix counter type to CPS'''
    return OUT_COUNTER_TYPE_MAP[data]

def _fix_counter_type_from_cps(data):
    '''Convert counter type from CPS'''
    return IN_COUNTER_TYPE_MAP[data]


IN_PACKET_ACTION_TYPE_MAP = {1:"DROP", 
2:"FORWARD", 
3:"COPY_TO_CPU", 
4:"COPY_TO_CPU_CANCEL", 
5:"TRAP_TO_CPU", 
6:"COPY_TO_CPU_AND_FORWARD", 
7:"COPY_TO_CPU_CANCEL_AND_DROP", 
8:"COPY_TO_CPU_CANCEL_AND_FORWARD", 
}
OUT_PACKET_ACTION_TYPE_MAP = {"DROP":1,
"FORWARD":2,
"COPY_TO_CPU":3,
"COPY_TO_CPU_CANCEL":4,
"TRAP_TO_CPU":5,
"COPY_TO_CPU_AND_FORWARD":6,
"COPY_TO_CPU_CANCEL_AND_DROP":7,
"COPY_TO_CPU_CANCEL_AND_FORWARD":8,
}

def _fix_packet_action_type_to_cps(data):
    '''Fix packet action type to CPS'''
    return OUT_PACKET_ACTION_TYPE_MAP[data]

def _fix_packet_action_type_from_cps(data):
    '''Convert packet action type from CPS'''
    return IN_PACKET_ACTION_TYPE_MAP[data]

IN_ACTION_TYPE_MAP = {1:"REDIRECT_PORT", 
2:"REDIRECT_IP_NEXTHOP", 
3:"PACKET_ACTION", 
4:"FLOOD", 
5:"MIRROR_INGRESS", 
6:"MIRROR_EGRESS", 
7:"SET_COUNTER", 
8:"SET_POLICER", 
9:"DECREMENT_TTL", 
10:"SET_TC", 
11:"SET_INNER_VLAN_ID", 
12:"SET_INNER_VLAN_PRI", 
13:"SET_OUTER_VLAN_ID", 
14:"SET_OUTER_VLAN_PRI", 
15:"SET_SRC_MAC", 
16:"SET_DST_MAC", 
17:"SET_SRC_IP", 
18:"SET_DST_IP", 
19:"SET_SRC_IPV6", 
20:"SET_DST_IPV6", 
21:"SET_DSCP", 
22:"SET_L4_SRC_PORT", 
23:"SET_L4_DST_PORT", 
24:"SET_CPU_QUEUE", 
25:"EGRESS_MASK", 
26:"REDIRECT_PORT_LIST", 
27:"REDIRECT_INTF", 
28:"EGRESS_INTF_MASK", 
29:"REDIRECT_INTF_LIST", 
30:"SET_USER_TRAP_ID", 
31:"SET_PACKET_COLOR", 
}
OUT_ACTION_TYPE_MAP = {"REDIRECT_PORT":1,
"REDIRECT_IP_NEXTHOP":2,
"PACKET_ACTION":3,
"FLOOD":4,
"MIRROR_INGRESS":5,
"MIRROR_EGRESS":6,
"SET_COUNTER":7,
"SET_POLICER":8,
"DECREMENT_TTL":9,
"SET_TC":10,
"SET_INNER_VLAN_ID":11,
"SET_INNER_VLAN_PRI":12,
"SET_OUTER_VLAN_ID":13,
"SET_OUTER_VLAN_PRI":14,
"SET_SRC_MAC":15,
"SET_DST_MAC":16,
"SET_SRC_IP":17,
"SET_DST_IP":18,
"SET_SRC_IPV6":19,
"SET_DST_IPV6":20,
"SET_DSCP":21,
"SET_L4_SRC_PORT":22,
"SET_L4_DST_PORT":23,
"SET_CPU_QUEUE":24,
"EGRESS_MASK":25,
"REDIRECT_PORT_LIST":26,
"REDIRECT_INTF":27,
"EGRESS_INTF_MASK":28,
"REDIRECT_INTF_LIST":29,
"SET_USER_TRAP_ID":30,
"SET_PACKET_COLOR":31,
}

def _fix_action_type_to_cps(data):
    '''Fix action type to CPS'''
    return OUT_ACTION_TYPE_MAP[data]

def _fix_action_type_from_cps(data):
    '''Convert action type from CPS'''
    return IN_ACTION_TYPE_MAP[data]


IN_MATCH_IP_FRAG_MAP = {1:"ANY", 
2:"NON_FRAG", 
3:"NON_FRAG_OR_HEAD", 
4:"HEAD", 
5:"NON_HEAD", 
}
OUT_MATCH_IP_FRAG_MAP = {"ANY":1,
"NON_FRAG":2,
"NON_FRAG_OR_HEAD":3,
"HEAD":4,
"NON_HEAD":5,
}


def _fix_match_ip_frag_to_cps(data):
    '''Fix match ip frag type to CPS'''
    return OUT_MATCH_IP_FRAG_MAP[data]

def _fix_match_ip_frag_from_cps(data):
    '''Convert match ip frag type from CPS'''
    return IN_MATCH_IP_FRAG_MAP[data]


IN_MATCH_IP_TYPE_MAP = {1:"ANY", 
2:"IP", 
3:"NON_IP", 
4:"IPV4ANY", 
5:"NON_IPV4", 
6:"IPV6ANY", 
7:"NON_IPV6", 
8:"ARP", 
9:"ARP_REQUEST", 
10:"ARP_REPLY", 
}
OUT_MATCH_IP_TYPE_MAP = {"ANY":1,
"IP":2,
"NON_IP":3,
"IPV4ANY":4,
"NON_IPV4":5,
"IPV6ANY":6,
"NON_IPV6":7,
"ARP":8,
"ARP_REQUEST":9,
"ARP_REPLY":10,
}

def _fix_ip_type_to_cps(data):
    '''Fix ip type to CPS'''
    return OUT_MATCH_IP_TYPE_MAP[data]

def _fix_ip_type_from_cps(data):
    '''Convert ip type from CPS'''
    return IN_MATCH_IP_TYPE_MAP[data]


IN_STAGE_MAP = {1:"INGRESS", 
2:"EGRESS", 
}
OUT_STAGE_MAP = {"INGRESS":1,
"EGRESS":2,
}

def _fix_stage_to_cps(data):
    '''Fix stage to CPS'''
    return OUT_STAGE_MAP[data]

def _fix_stage_from_cps(data):
    '''Convert stage from CPS'''
    return IN_STAGE_MAP[data]


IN_PACKET_COLOR_MAP = {1:"GREEN", 
2:"YELLOW", 
3:"RED"
}
OUT_PACKET_COLOR_MAP = {"GREEN":1,
"YELLOW":2,
"RED":3
}

def _fix_packet_color_to_cps(data):
    '''Fix stage to CPS'''
    return OUT_PACKET_COLOR_MAP[data]

def _fix_packet_color_from_cps(data):
    '''Convert stage from CPS'''
    return IN_PACKET_COLOR_MAP[data]

IN_RANGE_TYPE_MAP = {1:"L4_SRC_PORT", 
2:"L4_DST_PORT", 
3:"OUTER_VLAN", 
4:"INNER_VLAN", 
5:"PACKET_LENGTH", 
}
OUT_RANGE_TYPE_MAP = {"L4_SRC_PORT":1,
"L4_DST_PORT":2,
"OUTER_VLAN":3,
"INNER_VLAN":4,
"PACKET_LENGTH":5,
}

def _fix_range_type_to_cps(data):
    '''Fix range type to CPS'''
    return OUT_RANGE_TYPE_MAP[data]

def _fix_range_type_from_cps(data):
    '''Convert range type from CPS'''
    return IN_RANGE_TYPE_MAP[data]

IN_FILTER_TYPE_MAP = {1:"DISABLE", 
2:"ENABLE", 
3:"INGRESS_ENABLE", 
4:"EGRESS_ENABLE", 
}
OUT_FILTER_TYPE_MAP = {"DISABLE":1,
"ENABLE":2,
"INGRESS_ENABLE":3,
"EGRESS_ENABLE":4,
}

def _fix_filter_type_to_cps(data):
    '''Fix range type to CPS'''
    return OUT_FILTER_TYPE_MAP[data]

def _fix_filter_type_from_cps(data):
    '''Convert range type from CPS'''
    return IN_FILTER_TYPE_MAP[data]

DO_FILTER_TYPE = (_fix_filter_type_to_cps, _fix_filter_type_from_cps)
DO_RANGE_TYPE = (_fix_range_type_to_cps, _fix_range_type_from_cps)
DO_PACKET_COLOR = (_fix_packet_color_to_cps, _fix_packet_color_from_cps)
DO_STAGE = (_fix_stage_to_cps, _fix_stage_from_cps)
DO_IP_TYPE = (_fix_ip_type_to_cps, _fix_ip_type_from_cps)
DO_IP_FRAG = (_fix_match_ip_frag_to_cps, _fix_match_ip_frag_from_cps)
DO_ACTION_TYPE = (_fix_action_type_to_cps, _fix_action_type_from_cps)
DO_PACKET_ACTION_TYPE = (_fix_packet_action_type_to_cps, _fix_packet_action_type_from_cps)
DO_COUNTER_TYPE = (_fix_counter_type_to_cps, _fix_counter_type_from_cps)
DO_MATCH_TYPE = (_fix_match_type_to_cps, _fix_match_type_from_cps)
DO_FEC = (_fix_fec_to_cps, _fix_fec_from_cps)
DO_LEARN_MODE = (_fix_learn_mode_to_cps, _fix_learn_mode_from_cps)
DO_CLEAR_COUNTERS = (_fix_clear_counters_to_cps, _fix_clear_counters_from_cps)
DO_BREAKOUT_MODE = (_fix_breakout_mode_to_cps, _fix_breakout_mode_from_cps)
DO_TAGGING_MODE = (_fix_tagging_mode_to_cps, _fix_tagging_mode_from_cps)
DO_MEDIA = (_fix_media_to_cps, _fix_media_from_cps)
DO_SPEED = (_fix_speed_to_cps, _fix_speed_from_cps)
DO_MODE = (_fix_mode_to_cps, _fix_mode_from_cps)
DO_DUPLEX_TYPE = (_fix_duplex_type_to_cps, _fix_duplex_type_from_cps)
DO_VLAN_TYPE = (_fix_vlan_type_to_cps, _fix_vlan_type_from_cps)
DO_BOOL = (_bool_to_cps, _bool_from_cps)
STRIP_MODULE = (_strip_module_to_cps, _strip_module_from_cps)
FIX_IF_TYPE = (_fix_iftype_to_cps, _fix_iftype_from_cps)

GLOBAL_MAP = TypeMap({'base-ip/ipv4/forwarding': DO_BOOL,
           'dell-if/if/interfaces/interface/learning-mode':DO_BOOL,
           'if/interfaces/interface/enabled':DO_BOOL,
           'ietf-interfaces/interface/type':FIX_IF_TYPE,  # need to check this one, it may be surplus now
           'if/interfaces/interface/type':FIX_IF_TYPE,
           'dell-if/if/interfaces/interface/vlan-type':DO_VLAN_TYPE,
           'dell-if/if/interfaces/interface/duplex':DO_DUPLEX_TYPE,
           'dell-if/if/interfaces/interface/auto-negotiation':DO_BOOL,
           'dell-if/if/interfaces/interface/mode':DO_MODE,
           'dell-if/if/interfaces/interface/speed':DO_SPEED,
           'base-if-phy/if/interfaces/interface/phy-media':DO_MEDIA,
           'base-if-phy/if/interfaces/interface/tagging-mode':DO_TAGGING_MODE,
           'base-if-phy/if/interfaces/interface/learn-mode':DO_LEARN_MODE,
           'base-if-phy/breakout/fanout-mode':DO_BREAKOUT_MODE,
           'base-if-phy/set-breakout-mode/breakout-mode':DO_BREAKOUT_MODE,
           'dell-if/if/interfaces/interface/fec':DO_FEC,
           'dell-if/clear-counters/all-intf':DO_CLEAR_COUNTERS,
           'dell-if/clear-eee-counters/all-intf':DO_CLEAR_COUNTERS,
           'base-acl/entry/match/IP_FRAG_VALUE':DO_IP_FRAG,
           'base-acl/entry/match/type':DO_MATCH_TYPE,
           'base-acl/entry/match/IP_PROTOCOL_VALUE':DO_MATCH_TYPE,
           'base-acl/entry/match/IP_TYPE_VALUE':DO_IP_TYPE,
           'base-acl/entry/action/COUNTER_VALUE':DO_COUNTER_TYPE,
           'base-acl/entry/action/PACKET_ACTION_VALUE':DO_PACKET_ACTION_TYPE,
           'base-acl/entry/action/type':DO_ACTION_TYPE,
           'base-acl/table/allowed-match-fields':DO_MATCH_TYPE,
           'base-acl/table/stage':DO_STAGE,
           'dell-base-if-cmn/if/interfaces/interface/vlan-filter':DO_FILTER_TYPE,
           })


