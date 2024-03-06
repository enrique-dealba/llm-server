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

new_master_funcs = [
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