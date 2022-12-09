#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2022 iRobot Corporation. All rights reserved.
#

# Helper constants for making music with robots

class Note:
    SIXTEENTH = 0.0625  # semiquaver
    EIGHTH = 2 * SIXTEENTH  # quaver
    QUARTER = 2 * EIGHTH  # crotchet
    HALF = 2 * QUARTER  # minim
    WHOLE = 2 * HALF  # semibreve

    # Freq constants.
    C1 = 32  # Hz
    C1_SHARP = 34
    D1 = 36
    D1_SHARP = 38
    E1 = 41
    F1 = 43
    F1_SHARP = 46
    G1 = 48
    G1_SHARP = 51
    A1 = 55
    A1_SHARP = 58
    B1 = 61

    C2 = 65
    C2_SHARP = 69
    D2 = 73
    D2_SHARP = 77
    E2 = 82
    F2 = 87
    F2_SHARP = 92
    G2 = 97
    G2_SHARP = 103
    A2 = 110
    A2_SHARP = 116
    B2 = 123

    C3 = 130
    C3_SHARP = 138
    D3 = 146
    D3_SHARP = 155
    E3 = 164
    F3 = 174
    F3_SHARP = 184
    G3 = 195
    G3_SHARP = 207
    A3 = 220
    A3_SHARP = 233
    B3 = 246

    C4 = 261
    C4_SHARP = 277
    D4 = 293
    D4_SHARP = 311
    E4 = 329
    F4 = 349
    F4_SHARP = 369
    G4 = 391
    G4_SHARP = 415
    A4 = 440
    A4_SHARP = 466
    B4 = 493

    C5 = 523
    C5_SHARP = 554
    D5 = 587
    D5_SHARP = 622
    E5 = 659
    F5 = 698
    F5_SHARP = 739
    G5 = 783
    G5_SHARP = 830
    A5 = 880
    A5_SHARP = 932
    B5 = 987

    C6 = 1046
    C6_SHARP = 1108
    D6 = 1174
    D6_SHARP = 1244
    E6 = 1318
    F6 = 1396
    F6_SHARP = 1479
    G6 = 1567
    G6_SHARP = 1661
    A6 = 1760
    A6_SHARP = 1864
    B6 = 1975

    C7 = 2093
    C7_SHARP = 2217
    D7 = 2349
    D7_SHARP = 2489
    E7 = 2637
    F7 = 2793
    F7_SHARP = 2959
    G7 = 3135
    G7_SHARP = 3322
    A7 = 3520
    A7_SHARP = 3729
    B7 = 3951

    C8 = 4186
    C8_SHARP = 4434
    D8 = 4698
    D8_SHARP = 4978
    E8 = 5274
    F8 = 5587
    F8_SHARP = 5919
    G8 = 6271
    G8_SHARP = 6644
    A8 = 7040
    A8_SHARP = 7458
    B8 = 7902

    C9 = 8372
