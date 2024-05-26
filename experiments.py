"""Objectives Testing."""

# Single examples + descriptions
# CMO avg correct, PRO avg correct:

open_hermes_1 = [1.0, .5833]
open_hermes_gptq_1 = [0.125, 0.042]
hermes_pro_1 = [1.0, 0.4583]

# Two examples + descriptions
open_hermes_2 = [1.0, 0.7083]
open_hermes_gptq_2 = [0.708, 0.50]
hermes_pro_2 = [0.9306, 0.625]

# Note: ONLY respond in JSON. added
# CMO FIELDS, PRO FIELD
open_hermes_3 = [0.8968, 0.7732]
open_hermes_gptq_3 = [0.1667, 0.3889]
hermes_pro_3 = [0.7460, 0.6134]

# Revert back to non-ONLY respond in JSON
open_hermes_4 = [1.0, 0.8571]
open_hermes_gptq_4 = [0.4561, 0.5820]
hermes_pro_4 = [0.9365, 0.7868]

# num_tests=1 with Time Fields (measuring field and objective correctness):
# CMO fields, CMO obj (sussy), PRO fields, PRO obj
open_hermes_5 = [0.9464, 1.0, .5873, 1.0]
open_hermes_gptq_5 = [0.6250, 1.0, 0.0, 0.0]
hermes_pro_5 = [1.0, 1.0, 0.8125, 0.8333]

# num_tests=30 with Time Fields (compare to v9)
open_hermes_6 = [0.9024, 1.0, .6149, .9760]
open_hermes_gptq_6 = [0.3542, 1.0, .2889, 1.0]
hermes_pro_6 = [0.9881, 1.0, 0.8383, 0.8798]

# num_tests=30 with Time Fields + "ONLY respond in JSON"
open_hermes_7 = [0.8137, 1.0, 0.6104, 0.9807]
open_hermes_gptq_7 = [0.3073, 1.0, 0.3256, 0.5556]
hermes_pro_7 = [0.9274, 1.0, 0.7564, 0.9714]

# num_tests=12 with Time Fields + Note: ONLY respond in JSON with the single field << "objective" >> / << {field_name} >>
open_hermes_8 = [0.6116, 1.0, 0.4907, 0.6795]
open_hermes_gptq_8 = [0.2703, 1.0, 0.2361, 0.6667]
hermes_pro_8 = [1.0, 1.0, 0.9426, 0.8690]

# num_tests=12 with Time Fields (RUN 2, expecting sim to before)
open_hermes_9 = [0.8973, 1.0, 0.6194, 0.9524]
open_hermes_gptq_9 = [0.3611, 1.0, 0.3333, 1.0]
hermes_pro_9 = [0.9895, 1.0, 0.8434, 0.9036]

# num_tests=5 with Time Fields (RUN 3, after fixing Objectives field extractions)
open_hermes_10 = [0.91, 1.0, 0.6127, 0.9429]
open_hermes_gptq_10 = [0.3450, 1.0, 0.3157, 0.0909]
hermes_pro_10 = [0.9929, 1.0, 0.8544, 0.8571]

# num_tests=5 with Time Fields (RUN 4, after fixing Model field extractions)
open_hermes_11 = [0.9036, 1.0, 0.6044, 0.9714]
open_hermes_gptq_11 = [0.7964, 1.0, 0.7139, 0.1143]
hermes_pro_11 = [1.0, 1.0, 0.9857, 0.8857]

# num_tests=5: After major Objective definitions update for CMO and PRO
# CMO fields, CMO obj (sussy), PRO fields, PRO obj
open_hermes_12 = [0.7443, 1.0, 0.2908, 1.0]
open_hermes_gptq_12 = [0.4091, 1.0, 0.3686, 0.8571]
hermes_pro_12 = [0.9922, 1.0, 0.6405, 1.0]

# num_tests=3: After major Objective definitions update for CMO and PRO
# After ObjectiveList implementation (dis-entanglement)
open_hermes_13 = [0.7965, 1.0, 0.3214, 1.0]
open_hermes_gptq_13 = [0.6263, 1.0, 0.4762, 1.0]
hermes_pro_13 = [1.0, 1.0, 0.6905, 1.0]

# num_tests=12: After major Objective definitions update for CMO and PRO
open_hermes_14 = [0.7857, 1.0, 0.3819, 1.0]
open_hermes_gptq_14 = [0.6077, 1.0, 0.4784, 0.6471]
hermes_pro_14 = [1.0, 1.0, 0.6994, 1.0]

"""
open_hermes_15 = [
    AAA, AAA, # CMO
    AAA, AAA, # PRO
    AAA, AAA, # SO
    AAA, AAA, # DEO
    AAA, AAA, # SCO
]
open_hermes_gptq_15 = [
    AAA, AAA, # CMO
    AAA, AAA, # PRO
    AAA, AAA, # SO
    AAA, AAA, # DEO
    AAA, AAA, # SCO
]
hermes_pro_15 = [
    AAA, AAA, # CMO
    AAA, AAA, # PRO
    AAA, AAA, # SO
    AAA, AAA, # DEO
    AAA, AAA, # SCO
]
"""

# num_tests=1: Complete Objectives:
# CMO, PRO, SO, DEO, SCO
open_hermes_15 = [
    0.7792, 1.0, # CMO
    0.3571, 1.0, # PRO
    0.7898, 0.0, # SO
    0.0, 0.0, # DEO
    0.7848, 0.0, # SCO
]
open_hermes_gptq_15 = [
    0.6667, 1.0, # CMO
    0.4329, 0.6667, # PRO
    0.4196, 0.0, # SO
    0.4535, 0.0, # DEO
    0.3961, 0.0, # SCO
]
hermes_pro_15 = [
    1.0, 1.0, # CMO
    0.6786, 1.0, # PRO
    0.9619, 0.0, # SO
    0.8653, 0.0, # DEO
    0.9083, 0.0, # SCO
]

# num_tests=5: Complete Objectives + fixed Obj extraction prompt
# CMO, PRO, SO, DEO, SCO
open_hermes_16 = [
    0.7844, 1.0, # CMO
    0.3512, 1.0, # PRO
    0.7391, 1.0, # SO
    0.6068, 1.0, # DEO
    0.5344, 1.0, # SCO
]
open_hermes_gptq_16 = [
    0.500, 1.0, # CMO
    0.445, 0.0, # PRO
    0.274, 1.0, # SO
    0.4918, 0.8974, # DEO
    0.3959, 0.8696, # SCO
]
hermes_pro_16 = [
    1.0, 1.0, # CMO
    0.7266, 0.900, # PRO
    0.9119, 0.9750, # SO
    0.9705, 0.750, # DEO
    0.9797, 0.900, # SCO
]

# num_tests=1: Code refactor + try/except logic for fields + Optional[Union[type, str]]
open_hermes_17 = [
    0.7792, 1.0, # CMO
    0.4714, 1.0, # PRO
    0.7422, 1.0, # SO
    0.6023, 1.0, # DEO
    0.5385, 1.0, # SCO
]
open_hermes_gptq_17 = [
    0.6727, 1.0, # CMO
    0.4946, 0.3333, # PRO
    0.25, 1.0, # SO
    0.4675, 0.7143, # DEO
    0.4098, 0.600, # SCO
]
hermes_pro_17 = [
    1.0, 1.0, # CMO
    0.7449, 1.0, # PRO
    0.9219, 1.0, # SO
    0.9773, 0.75, # DEO
    0.9659, 0.6250, # SCO
]

# num_tests=15: Base vs. GPTQ vs. AWQ for OpenHermes 2.5
# base_openhermes_1 = [
#     None, None, # CMO
#     AAA, AAA, # PRO
#     AAA, AAA, # SO
#     AAA, AAA, # DEO
#     AAA, AAA, # SCO
# ]
# gptq_openhermes_1 = [
#     AAA, AAA, # CMO
#     AAA, AAA, # PRO
#     AAA, AAA, # SO
#     AAA, AAA, # DEO
#     AAA, AAA, # SCO
# ]
awq_openheres_1 = [
    0.6762, 1.0, # CMO
    0.3793, 1.0, # PRO
    0.4595, 1.0, # SO
    0.6346, 1.0, # DEO
    0.4576, 1.0, # SCO
]

# Field %, obj %, avg completion time per response (seconds)

base_openhermes_2 = [
    0.7965, 1.0, 4.68,  # CMO
    0.4539, 1.0, 4.77, # PRO
    0.7278, 1.0, 6.05, # SO
    0.6216, 1.0, 4.99, # DEO
    0.5331, 1.0, 4.98, # SCO
]
# gptq_openhermes_2 = [
#     AAA, AAA, # CMO
#     AAA, AAA, # PRO
#     AAA, AAA, # SO
#     AAA, AAA, # DEO
#     AAA, AAA, # SCO
# ]
awq_openheres_2 = [
    0.6710, 1.0, 7.67, # CMO
    0.3886, 1.0, 5.86, # PRO
    0.4624, 1.0, 7.10, # SO
    0.6314, 1.0, 7.49, # DEO
    0.4750, 1.0, 5.78, # SCO
]

# RUN=2: Field %, obj %, avg completion time per response (seconds)

base_openhermes_3 = [
    0.8009, 1.0, 4.77, # CMO
    0.4537, 1.0, 4.78, # PRO
    0.7244, 1.0, 6.05, # SO
    0.6104, 1.0, 5.03, # DEO
    0.5229, 1.0, 4.94, # SCO
]
gptq_openhermes_3 = [
    0.6122, 1.0, 5.99, # CMO
    0.5404, 0.2473, 5.58, # PRO
    0.2836, 0.92, 4.99, # SO
    0.4811, 0.8230, 4.71, # DEO
    0.4296, 0.7692, 4.15, # SCO
]
awq_openheres_3 = [
    0.6797, 1.0, 7.53, # CMO
    0.3801, 1.0, 5.96, # PRO
    0.4448, 1.0, 6.87, # SO
    0.6347, 0.9909, 7.50, # DEO
    0.4615, 1.0, 5.86, # SCO
]

# Mistral (AWQ,GPTQ) vs. OpenHermes (AWQ,GPTQ) @num_tests=15
gptq_mistral_1 = [
    1.0, 1.0, 2.76, # CMO
    1.0, 0.5, 3.92, # PRO
    0.9375, 1.0, 3.82, # SO
    1.0, 1.0, 2.97, # DEO
    1.0, 1.0, 3.28, # SCO
]
awq_mistral_1 = [
    1.0, 1.0, 5.77, # CMO
    1.0, 0.2344, 7.25, # PRO
    0.9375, 1.0, 5.85, # SO
    1.0, 1.0, 4.68, # DEO
    1.0, 1.0, 5.01, # SCO
]
gptq_openhermes_1 = [
    0.7066, 1.0, 13.58, # CMO
    0.7308, 0.0, 8.99, # PRO
    0.7833, 0.0, 13.54, # SO
    0.7089, 0.0, 18.22, # DEO
    0.8189, 0.0, 10.09 # SCO
]
awq_openhermes_1 = [
    0.7818, 1.0, 24.62, # CMO
    0.6401, 0.2255, 28.49, # PRO
    0.5802, 0.2689, 28.04, # SO
    0.7563, 0.2672, 30.31, # DEO
    0.6764, 0.3417, 32.06, # SCO
]

# OpenHermes-2.5-Mistral-7B Results

funcs_16 = [
    0.6,
    0.67,
    0.63,
    .63,
    .65,
    .63,
    .63,
    .65,
    .65,
    .62,
    .43,
    .62,
    .61,
    .6,
    .64,
    .65,
    .64,
    .63,
    .65,
]

funcs_15 = [
    .65,
    .61,
    .65,
    .66,
    .64,
    .64,
    .65,
    .67,
    .64,
    .62,
    .6,
    .67,
    .61,
    .64,
    .64,
    .62,
    .64,
    .62,
    .68,
    .63,
]

funcs_14 = [
    0.6,
    0.65,
    0.65,
    0.69,
    0.61,
    0.63,
    0.63,
    0.65,
    0.66,
    0.67,
    0.57,
    0.62,
    0.67,
    0.67,
    0.63,
    0.6,
    0.71,
    0.66,
    0.64,
    0.61,
    0.61,
    0.62,
    0.59,
    0.63,
    0.66,
    0.7,
    0.63
]

funcs_13 = [
    .64,
    .58,
    .57,
    .59,
    .66,
    .63,
    .62,
    .56,
    .71,
    .68,
    .58,
    .62,
    .66,
    .66,
    .6,
    .68,
    .69,
    .64,
    .64,
    .61,
]

funcs_12 = [
    .63,
    .65,
    .59,
    .61,
    .67,
    .65,
    .59,
    .68,
    .64,
    .62,
    .62,
    .61, # 12/20
    .62,
    .72,
    .57, # 16/20
    .65,
    .71,
    .63,
    .7,
    .59,
]

funcs_11 = [
    .59,
    .58,
    .65,
    .61,
    .65,
    .59,
    .71,
    .59,
    .59,
    .64,
    .54,
    .68,
    .63,
    .67,
    .56, # from 15/20
    .57,
    .62,
    .61,
    .7,
    .61,
]

funcs_10 = [
    .69,
    .57,
    .6,
    .63,
    .71,
    .71,
    .79,
    .59,
    .51,
    .61,
    .7,
    .66,
    .63,
    .62,
    .63,
    .55,
    .6,
    .52,
    .69,
]

funcs_9 = [
    .72,
    .58,
    .6,
    .75,
    .79,
    .63,
    .68,
    .64,
    .72,
    .67,
    .55,
    .62,
    .6,
    .5,
    .66,
    .65,
    .78,
    .64,
    .58,
    .68,
]

funcs_8 = [
    .62, ## starting at 14/20 to 1/20
    .73,
    .62,
    .56,
    .6,
    .58,
    .66,
    .63,
    .75,
    .66,
    .76,
    .6,
    .61,
    .67, # starting at 15/20
    .7,
    .72,
    .5,
    .73,
    .57,
]

funcs_7 = [
    .67,
    .55,
    .59,
    .59,
    .53,
    .58,
    .67,
    .53,
    .71,
    .68,
    .73,
    .7,
    .56,
    .54,
    .73,
    .34,
    .58,
    .52,
    .68,
    .69,
]

funcs_6 = [
    .6,
    .74,
    .76,
    .71,
    .62,
    .64,
    .48,
    .57,
    .7,
    .64,
    .68,
    .61,
    .72,
    .66,
    .74,
    .76,
    .6,
    .59,
    .62,
    .72,
]

funcs_5 = [
    .55,
    .72,
    .77,
    .6,
    .53,
    .47,
    .63,
    .44,
    .72,
    .31,
    .49,
    .56,
]

funcs_4 = [
    .47,
    .45,
    .67,
    .55,
    .62,
    .53,
    .58,
    .58,
    .8,
    .38,
    .47,
    .48,
    .58,
    .77,
    .78,
    .75,
    .52,
    .58,
    .62,
    .77,
]

funcs_3 = [
    .53,
    .8,
    .76,
    .78,
    .58,
    .53,
    .64,
    .8,
    .49,
    .44,
    .71,
    .71,
    .51,
    .51,
    .6,
    .73,
    .69,
]

funcs_2 = [
    .87,
    .6,
    .63,
    .33,
    .67,
    .87,
    .8,
    .8,
    .5,
    .3,
    .53,
    .3,
    .63,
    .83,
    .4,
    .33,
    .4,
    .8,
    .57,
    .47,
    .47, # additional experiments and beyond
    .77, 
    .5,
    .93,
    .73,
    .63,
    .77,
    .7,
    .77,
    .57,
    .53,
    .67,
    .77,
    .57,
    .67,
    .5,
    .87,
    .87,
    .53,
    .57,
    .8,
    .8,
    .7,
    .8,
]

funcs_1 = [
    .53, # get_ascii
    .93, # compress_whitespace
    .6, # generate_acronym
    .33, # get_day_of_week
    .33, # get_day_of_week
    .67, # last_letter
    .67, # count_words
    .67, # divide_by_two
    .93, # compree_whitespace
    1.0, # capitlalize_first_letter
    .33, # get_day_of_week
    1.0, # capitlalize_first_letter
    .6, # convert_to_binary
    .33, # extract_domain
    1.0, # convert_to_uppercase
    .53, # get_ascii
    1.0, # convert_to_uppercase
    .6, # generate_acronym
    .33, # time
    .67, # count_words
    .53, # get_ascii
    1.0, # capitlalize_first_letter
    .6, # generate_acronym
    .33, # extract_domain
    .73, # get_vowel_count
    0.0, # extract_domain
    .33, # extract_domain
    .67, # count_words
    .33, # time
    .8, # reverse_string
    .33, # get_day_of_week
    0.0, # convert_to_uppercase
    1.0, # convert_to_uppercase
    .33, # get_day_of_week
    .33, # get_day_of_week
    .73, # get_vowel_count
    .33, # get_day_of_week
    .93, # compress_whitespace
    .67, # divide_by_two
    .6, # convert_to_binary
    .33, # get_day_of_week
    .93, # compress_whitespace
    1.0, # convert_to_uppercase
    1.0, # convert_to_uppercase
]

funcs_master = [
    .53, # get_ascii
    .93, # compress_whitespace
    .6, # generate_acronym

    .33, # get_day_of_week
    .67, # last_letter
    .67, # count_words

    .67, # divide_by_two
    1.0, # capitlalize_first_letter
    .6, # convert_to_binary

    .33, # extract_domain
    1.0, # convert_to_uppercase
    .33, # time

    .73, # get_vowel_count
    .8, # reverse_string
    .87, # format_phone_number
    0.0, # get_lat_long
]

## Mistral Instruct v0.2

mistral_master_funcs = [
    1.0, # divide_by_two
    0.0, # count_words
    .87, # get_day_of_week
    .8, # time

    1.0, # get_ascii
    0.0, # convert_to_uppercase
    .4, # reverse_string
    .47, # compress_whitespace

    0.0, # get_lat_long
    1.0, # last_letter
    .13, # capitlalize_first_letter
    0.0, # generate_acronym

    1.0, # format_phone_number
    1.0, # convert_to_binary
    1.0, # get_vowel_count
    .13, # extract_domain
]

m_funcs_1 = [
    .13,
    0.0,
    1.0,
    1.0,
    1.0,
    .13,
    0.0,
    1.0,
    0.0,
    1.0,
    1.0,
    1.0,
    0.0,
    1.0,
    0.0,
    .4,
    0.0,
    1.0,
    0.0,
    .13,
]

m_funcs_2 = [
    .4,
    .47,
    .97,
    .23,
    .33,
    .47,
    .57,
    .93,
    .73,
    .5,
    .5,
    .73,
    .97,
    .6,
    .43,
    .23,
    0.0,
    .97,
    .23,
    0.0,
]

m_funcs_3 = [
    .93,
    .31,
    .73,
    .29,
    .36,
    .67,
    .29,
    .67,
    .69,
    .58,
    .96,
    1.0,
    .64,
    .11,
    .47,
    .38,
    .96,
    .18,
    .42,
    .49,
]

m_funcs_4 = [
    .55,
    .97,
    .7,
    .7,
    .28,
    .98,
    .5,
    .37,
    .6,
    .3,
    .68,
    .83,
    .35,
    .65,
    .73,
    .67,
    .4,
    .47,
    .55,
    .33,
]

m_funcs_5 = [
    .6,
    .6,
    .36,
    .28,
    .81,
    .51,
    .61,
    .57,
    .52,
    .64,
    .67,
    .68,
    .44,
    .13,
    .61,
    .69,
    .63,
    .4,
    .47,
    .67,
]

m_funcs_6 = [
    .6,
    .5,
    .51,
    .38,
    .67,
    .66,
    .37,
    .46,
    .62,
    .51,
    .52,
    .69,
    .33,
    .37,
    .63,
    .39,
    .46,
    .51,
    .51,
    .71,
]

m_funcs_7 = [
    .52,
    .66,
    .65,
    .67,
    .65,
    .52,
    .37,
    .65,
    .59,
    .38,
    .5,
    .52,
    .5,
    .49,
    .6,
    .67,
    .43,
    .69,
    .65,
    .48,
]

m_funcs_8 = [
    .52,
    .57,
    .57,
    .55,
    .54,
    .53,
    .65,
    .67,
    .47,
    .5,
    .53,
    .6,
    .5,
    .57,
    .55,
    .65,
    .53,
    .67,
    .55,
    .61,
]

m_funcs_9 = [
    .48,
    .58,
    .66,
    .43,
    .51,
    .52,
    .47,
    .61,
    .66,
    .47,
    .49,
    .57,
    .6,
    .72,
    .56,
    .54,
    .59,
    .56,
    .41,
    .61,
]

m_funcs_10 = [
    .76,
    .63,
    .61,
    .45,
    .49,
    .53,
    .55,
    .48,
    .59,
    .6,
    .43,
    .59,
    .61,
    .39,
    .61,
    .61,
    .56,
    .57,
    .45,
    .66,
]

m_funcs_11 = [
    .59,
    .62,
    .65,
    .52,
    .6,
    .51,
    .64,
    .49,
    .45,
    .7,
    .64,
    .45,
    .54,
    .5,
    .5,
    .42,
    .6,
    .38,
    .44,
    .56,
]

m_funcs_12 = [
    .51,
    .61,
    .55,
    .44,
    .43,
    .51,
    .46,
    .56,
    .57,
    .64,
    .44,
    .52,
    .54,
    .59,
    .55,
    .51,
    .66,
    .57,
    .61,
    .56,
]
m_funcs_16 = [
    .55,
    .56,
    .56,
    .56,
    .55,
    .57,
    .57,
    .55,
    .55,
    .56,
    .56,
    .55,
    .56,
    .55,
    .55,
    .55,
    .56,
    .54,
    .54,
    .54,
]

m_funcs_15 = [
    .53,
    .52,
    .55,
    .58,
    .59,
    .52,
    .54,
    .58,
    .51,
    .56,
    .52,
    .52,
    .55,
    .6,
    .61,
    .56,
    .56,
    .58,
    .59,
    .52,
]

m_funcs_14 = [
    .5,
    .54,
    .56,
    .61,
    .56,
    .57,
    .49,
    .5,
    .61,
    .6,
    .5,
    .5,
    .56,
    .54,
    .61,
    .57,
    .51,
    .57,
    .48,
    .49,
]

m_funcs_13 = [
    .44,
    .49,
    .43,
    .62,
    .59,
    .67,
    .65,
    .49,
    .53,
    .52,
    .52,
    .5,
    .55,
    .52,
    .51,
    .56,
    .52,
    .59,
    .61,
    .54,
]

"""New Tests.

Here we're doing single pass tests per function + all funcs testing.
"mistralai/Mistral-7B-Instruct-v0.2" - m1
"teknium/OpenHermes-2.5-Mistral-7B" - h1
"TheBloke/Mistral-7B-v0.1-GPTQ" - m1_gptq
"TheBloke/OpenHermes-2.5-Mistral-7B-GPTQ" - h1_gptq
Follow-up tests will increment the number: h{n}/m{n}{_gptq}
"""

m1_funcs1 = [
    1.0,
    .13,
    .47,
    0.0,
    0.0,
    .87,
    1.0,
    1.0,
    0.0,
    0.0,
    .13,
    .8,
    .4,
    1.0,
    1.0,
    1.0,
]

m1_funcs16 = [
    .55,
    .53,
]

h1_funcs1 = [
    .4,
    1.0,
    0.0,
    1.0,
    0.0,
    .87,
    1.0,
    1.0,
    .8,
    .13,
    1.0,
    1.0,
    0.0,
    0.0,
    .47,
    .13,
]

h1_funcs16 = [
    .54,
    .55,
]

m1_gptq_funcs1 = [
    .93,
    .73,
    .2,
    0.0,
    0.0,
    .67,
    .8,
    .47,
    .53,
    .2,
    .47,
    .73,
    .13,
    .33,
    0.0,
    1.0,
]

m1_gptq_funcs16 = [
    .41,
    .37,
]

h1_gptq_funcs1 = [
    .13,
    0.0,
    .47,
    .8,
    .67,
    0.0,
    .73,
    .13,
    .53,
    .93,
    .6,
    1.0,
    .47,
    .27,
    0.0,
    .2,
]

h1_gptq_funcs16 = [
    .42,
    .4,
]

m2_funcs16 = [
    .56,
    .59,
]

h2_funcs16 = [
    .56,
    .56,
]

m2_gptq_funcs16 = [
    .43,
    .47,
]

h2_gptq_funcs16 = [
    .4,
    .43,
]

m3_funcs16 = [
    .56,
    .58,
]

h3_funcs1 = [
    .73,
    .67,
    .6,
    1.0,
    .6,
    .8,
    .93,
    .67,
    .67,
    .33,
    1.0,
    .53,
    0.0, # get_lat_long
    1.0,
    .87,
    .67,
]

h3_funcs16 = [
    .69,
    .71,
    .66,
    .67,
    .7,
    .7,
    .69,
]

m3_gptq_funcs16 = [
    .45,
    .43,
]

h3_gptq_func1 = [
    1.0,
    .93,
    1.0,
    .87,
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    0.0, # get_lat_long
    1.0,
    .93,
    1.0,
    .8,
    .93,
]

h3_gptq_funcs16 = [
    .89,
    .89,
    .9,
    .9,
    .88,
    .89,
]

m4_funcs16 = [
    .63,
    .62,
]

h4_funcs16 = [
    .71,
    .73,
]

m4_gptq_funcs16 = [
    .46,
    .45,
]

h4_gptq_funcs16 = [
    .95,
    .94,
]

## BELOW ARE FROM HERMES 2 NEW PROMPTING

h_pro_funcs16 = [
    .95,
    .95,
    .95,
    .95,
]

m5_gptq_funcs16 = [
    0.0,
    0.0,
]

# phi-2 gets 0.0 for everything still

h5_funcs16 = [
    .96,
    .96,
]

m5_funcs16 = [
    0.0,
    0.0,
]

h5_gptq_funcs16 = [
    .9875,
    .9875,
    .9916
]
