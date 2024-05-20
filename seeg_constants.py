# Sampling parameters
fs = 1024  # Natus sample rate

# Stroop task parameters
C_MAP = {1: 'red', 2: 'green', 3: 'blue'}

# Dictionaries
region_name = {'amygdala': 'Amygdala', 'ant_hippocampus': 'Anterior Hippocampus', 'pos_hippocampus': 'Posterior Hippocampus',
               'entorhinal': 'Entorhinal Cortex', 'para_hippocampus': 'Parahippocampus', 'amcc': 'Anterior Cingulate Cortex',
               'gyrus_rectus': 'Gyrus Rectus', 'precuneus': 'Precuneus', 'stg': 'Superior Temporal Gyrus',
               'heschl': 'Heschls Gyrus', 'mid_insula': 'Mid Insula', 'insula': 'Insula'}

# Common frequency bands (based on this: https://neuropsychology.github.io/NeuroKit/examples/eeg_power/eeg_power.html)
gamma = [30, 80]
beta = [13, 30]
alpha = [8, 13]
mu = [9, 11]
theta = [4, 8]
delta = [1, 4]
# test comment


##### Patient-specific parameters #####
class Subject:
    def __init__(self, patient):
        if patient == 'p9':  # games
            self.NUM_STROOP = 8
            self.NUM_BART = 5
            self.E_MAP = {'stroop1': 0, 'stroop2': 1, 'stroop3': 2, 'stroop4': 3, 'stroop5': 4, 'stroop6': 5,
                          'stroop7': 6, 'stroop8': 7, 'bart1': 8, 'bart2': 9, 'bart3': 10, 'bart4': 11, 'bart5': 12}
            self.DATE = "03/07/24"

            # FIXME: CHECK THESE WHEN MAPS COME IN
            self.amygdala_l = ["A'1", "A'2", "A'3", "A'4", "A'5", "A'6", "A'7", "A'8", "A'9", "A'10", "A'11", "A'12"]
            self.amygdala_r = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]
            self.amcc = ["G-G'1", "G-G'2", "G-G'3", "G-G'4", "G-G'5", "G-G'6", "G-G'7", "G-G'8", "G-G'9", "G-G'10",
                         "G-G'11", "G-G'12"]
            self.hippocampus_h_r = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"]
            self.hippocampus_t_l = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12"]
            self.para_hippocampus = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"]
            self.para_hippocampus_r = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"]
            self.gyrus_rectus_r = ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8", "O9", "O10", "O11", "O12"]
            self.heschl = ["U1", "U2", "U3", "U4", "U5", "U6", "U7", "U8", "U9", "U10"]
            self.pcc = ["X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10", "X11", "X12", "X13", "X14"]
            self.ant_insula_l = ["Y1", "Y2", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "Y10", "Y11", "Y12", "Y13", "Y14", "Y15", "Y16"]

        elif patient == 'p8':  # curious
            self.NUM_STROOP = 8
            self.NUM_BART = 0
            self.E_MAP = {'stroop1': 0, 'stroop2': 1, 'stroop3': 2, 'stroop4': 3, 'stroop5': 4, 'stroop6': 5,
                          'stroop7': 6, 'stroop8': 7}
            self.DATE = "02/22/24"

            self.amygdala_l = ["A'1", "A'2", "A'3", "A'4", "A'5", "A'6", "A'7", "A'8", "A'9", "A'10"]
            self.amygdala_r = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]
            self.hippocampus_h_l = ["B'1", "B'2", "B'3", "B'4", "B'5", "B'6", "B'7", "B'8", "B'9", "B'10"]
            self.hippocampus_h_r = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"]
            self.hippocampus_t_l = ["C'1", "C'2", "C'3", "C'4", "C'5", "C'6", "C'7", "C'8", "C'9", "C'10"]
            self.fusiform = ["F'1", "F'2", "F'3", "F'4", "F'5", "F'6", "F'7", "F'8"]
            self.amcc = ["G'1", "G'2", "G'3", "G'4", "G'5", "G'6", "G'7", "G'8", "G'9", "G'10", "G'11", "G'12"]  # first probe is ACC, remaining are WM, frontal sulcus
            self.gyrus_rectus_l = ["O'1", "O'2", "O'3", "O'4", "O'5", "O'6", "O'7", "O'8", "O'9", "O'10", "O'11",
                                   "O'12"]
            self.heschl = ["U'1", "U'2", "U'3", "U'4", "U'5", "U'6", "U'7", "U'8"]
            self.ant_insula_l = ["Y'1", "Y'2", "Y'4", "Y'5", "Y'6", "Y'7", "Y'8", "Y'9", "Y'10", "Y'11", "Y'12"]
            self.para_hippocampus = ["I'1", "I'2", "I'3", "I'4", "I'5", "I'6", "I'7", "I'8", "I'9", "I'10"]

        elif patient == 'p7':  # chill
            self.NUM_STROOP = 5
            self.NUM_BART = 0
            self.E_MAP = {'stroop1': 0, 'stroop2': 1, 'stroop3': 2, 'stroop4': 3, 'stroop5': 4}
            self.DATE = "12/13/23"

            self.amygdala_r = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]
            self.amygdala_l = ["A'1", "A'2", "A'3", "A'4", "A'5", "A'6", "A'7", "A'8"]
            self.hippocampus_h_r = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"]
            self.hippocampus_h_l = ["B'1", "B'2", "B'3", "B'4", "B'5", "B'6", "B'7", "B'8"]
            self.hippocampus_t_l = ["C'1", "C'2", "C'3", "C'4", "C'5", "C'6", "C'7", "C'8", "C'9", "C'10"]  # hippocampal B (I think this is tail)
            self.para_hippocampus = ["E'1", "E'2", "E'3", "E'4", "E'5", "E'6", "E'7", "E'8", "E'9"]
            self.fusiform = ["F'1", "F'2", "F'3", "F'4", "F'5", "F'6", "F'7", "F'8", "F'9"]
            self.para_hippocampus_r = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"]
            self.amcc = ["G-G'1", "G-G'2", "G-G'3", "G-G'4", "G-G'5", "G-G'6", "G-G'7", "G-G'8", "G-G'9", "G-G'10",
                         "G-G'11"]  # first 3 probes are L&R ACC
            self.temporal_pole = ["I'1", "I'2", "I'3", "I'4", "I'5", "I'6"]
            self.sma_l = ["M'1", "M'2", "M'3", "M'4", "M'5", "M'6", "M'7", "M'8", "M'9"]  # Supplementary motor area
            self.sma_r = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"]  # Supplementary motor area
            self.gyrus_rectus_r = ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8", "O9", "O10", "O11",
                                   "O12"]  # also Olf and Orb
            self.gyrus_rectus_l = ["O'1", "O'2", "O'3", "O'4", "O'5", "O'6", "O'7", "O'8", "O'9", "O'10", "O'11",
                                   "O'12", "O'13"]  # also OFC, IFG, Ptriag
            self.precuneus = ["P'1", "P'2", "P'3", "P'4", "P'5", "P'6", "P'7", "P'8"]  # also spg (?) and angular gyrus
            self.pcc = ["X'1", "X'2", "X'3", "X'4", "X'5", "X'6", "X'7", "X'8", "X'9", "X'10", "X'11",
                        "X'12"]  # Posterior cingulate
            self.ant_insula_l = ["Y'1", "Y'2", "Y'4", "Y'5", "Y'6", "Y'7", "Y'8", "Y'9", "Y'10", "Y'11", "Y'12", "Y'13"]

        elif patient == 'p6':  # snarky  *NOTE: THIS IS DATA ONLY FOR DAY 10/13, NOT 10/16!
            self.recording_start = '10:29:54.85'  # FIXME: CHECK THE MS
            # 10/16 start time: 10:14:58
            self.NUM_STROOP = 5
            self.NUM_BART = 4
            self.E_MAP = {'stroop1': 0, 'stroop2': 1, 'stroop3': 2, 'stroop4': 3, 'stroop5': 4, 'bart1': 5, 'bart2': 6,
                          'bart3': 7, 'bart4': 8}
            self.DATE = "10/13/23"

            self.amygdala_r = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]
            self.amygdala_l = ["A'1", "A'2", "A'3", "A'4", "A'5", "A'6", "A'7", "A'8", "A'9", "A'10"]
            self.hippocampus_h_r = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"]
            self.hippocampus_h_l = ["B'1", "B'2", "B'3", "B'4", "B'5", "B'6", "B'7", "B'8"]
            self.hippocampus_t_l = ["C'1", "C'2", "C'3", "C'4", "C'5", "C'6", "C'7", "C'8", "C'9", "C'10"]
            self.para_hippocampus = ["E'1", "E'2", "E'3", "E'4", "E'5", "E'6", "E'7", "E'8", "E'9", "E'10"]
            self.fusiform = ["F'1", "F'2", "F'3", "F'4", "F'5", "F'6", "F'7", "F'8"]
            self.amcc = ["G-G'1", "G-G'2", "G-G'3", "G-G'4", "G-G'5", "G-G'6", "G-G'7", "G-G'8", "G-G'9", "G-G'10",
                         "G-G'11", "G-G'12", "G-G'13", "G-G'14"]  # first 5 probes are L&R ACC
            self.gyrus_rectus_r = ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8", "O9", "O10", "O11", "O12"]  # also Olf and Orb
            self.gyrus_rectus_l = ["O'1", "O'2", "O'3", "O'4", "O'5", "O'6", "O'7", "O'8", "O'9", "O'10", "O'11", "O'12"]
            self.pcc = ["X'1", "X'2", "X'3", "X'4", "X'5", "X'6", "X'7", "X'8", "X'9", "X'10", "X'11", "X'12"]  # Posterior cingulate
            self.ant_insula_l = ["Y'1", "Y'2", "Y'4", "Y'5", "Y'6", "Y'7", "Y'8", "Y'9", "Y'10", "Y'11", "Y'12", "Y'13",
                                 "Y'14"]

        elif patient == 'p5':  # grumpy
            self.recording_start = '09:59:54.0'  # FIXME: CHECK THE MS
            self.NUM_STROOP = 5
            self.NUM_BART = 4
            self.E_MAP = {'stroop1': 0, 'stroop2': 1, 'stroop3': 2, 'stroop4': 3, 'stroop5': 4, 'bart1': 5, 'bart2': 6,
                          'bart3': 7, 'bart4': 8}
            self.DATE = "10/13/23"

            # FIXME: PPTX MAPPING WITH ' AND WITHOUT ' MIGHT SEEMS BACKWARDS COMPARED TO EDF CHANNELS
            self.amygdala_r = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]
            self.amygdala_l = ["A'1", "A'2", "A'3", "A'4", "A'5", "A'6", "A'7", "A'8", "A'9", "A'10"]
            self.hippocampus_h_r = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"]
            self.hippocampus_h_l = ["B'1", "B'2", "B'3", "B'4", "B'5", "B'6", "B'7", "B'8"]
            self.para_hippocampus = ["C'1", "C'2", "C'3", "C'4", "C'5", "C'6", "C'7", "C'8", "C'9", "C'10"]
            self.entorhinal_l = ["E'1", "E'2", "E'3", "E'4", "E'5", "E'6", "E'7", "E'8", "E'9", "E'10"]
            self.fusiform = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"]  # FIXME: THIS IS PHG PROBE, UNKNOWN WHAT THAT MEANS
            self.gyrus_rectus_r = ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8", "O9", "O10", "O11", "O12"]
            self.unknown1 = ["Y'1", "Y'2", "Y'4", "Y'5", "Y'6", "Y'7", "Y'8", "Y'9", "Y'10", "Y'11", "Y'12", "Y'13",
                                 "Y'14"]  #FIXME: UNKNOWN AREA
            self.unknown2 = ["X'1", "X'2", "X'3", "X'4", "X'5", "X'6", "X'7", "X'8", "X'9", "X'10", "X'11", "X'12"]  #FIXME: UNKNOWN AREA

        elif patient == 'p4':
            self.NUM_STROOP = 5
            self.NUM_BART = 1
            self.E_MAP = {'stroop1': 0, 'stroop2': 1, 'bart1': 2, 'stroop3': 3, 'stroop4': 4, 'stroop5': 5}
            self.DATE = "08/16/23"

            self.amygdala_l = ["A'1", "A'2", "A'3", "A'4", "A'5", "A'6", "A'7", "A'8", "A'9", "A'10"]
            self.amygdala_r = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]
            self.hippocampus_h_l = ["B'1", "B'2", "B'3", "B'4", "B'5", "B'6", "B'7", "B'8", "B'9", "B'10"]
            self.hippocampus_h_r = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"]
            self.pos_hippocampus = ["C'1", "C'2", "C'3", "C'4", "C'5", "C'6", "C'7", "C'8", "C'9", "C'10"]
            self.entorhinal_r = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"]
            self.entorhinal_l = ["E'1", "E'2", "E'3", "E'4", "E'5", "E'6", "E'7", "E'8"]
            self.fusiform = ["F'1", "F'2", "F'3", "F'4", "F'5", "F'6"]  # Only first probe is fusiform
            self.amcc = ["G-G'1", "G-G'2", "G-G'3", "G-G'4", "G-G'5", "G-G'6", "G-G'7", "G-G'8", "G-G'9", "G-G'10",
                         "G-G'11", "G-G'12", "G-G'13", "G-G'14"] # first 5 probes are L&R ACC
            self.temporal_pole = ["I'1", "I'2", "I'3", "I'4", "I'5", "I'6"]
            self.gyrus_rectus_l = ["O'1", "O'2", "O'3", "O'4", "O'5", "O'6", "O'7", "O'8", "O'9", "O'10", "O'11", "O'12"]  # also OFC and OlfS
            self.gyrus_rectus_r = ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8", "O9", "O10", "O11", "O'12"]
            self.stg = ["T'1", "T'2", "T'3", "T'4"]
            self.pcc = ["X'1", "X'2", "X'3", "X'4", "X'5", "X'6", "X'7", "X'8", "X'9", "X'10", "X'11", "X'12", "X'13", "X'14"]  # Posterior cingulate
            self.ant_insula_r = ["Y 1", "Y 2", "Y 3", "Y 4", "Y 5", "Y 6", "Y 7", "Y 8", "Y 9", "Y 10", "Y 11", "Y 12", "Y 13", "Y 14", "Y 15"]
            self.ant_insula_l = ["Y'1", "Y'2", "Y'4", "Y'5", "Y'6", "Y'7", "Y'8", "Y'9", "Y'10", "Y'11", "Y'12", "Y'13", "Y'14", "Y'15"]
        elif patient == 'p3':
            self.NUM_STROOP = 15
            self.NUM_BART = 3
            self.E_MAP = {'stroop1': 0, 'stroop2': 1, 'stroop3': 2, 'stroop4': 3, 'stroop5': 4, 'stroop6': 5,
                             'stroop7': 6, 'stroop8': 7, 'stroop9': 8, 'stroop10': 9, 'bart1': 10, 'bart2': 11,
                             'stroop11': 12, 'stroop12': 13, 'stroop13': 14, 'stroop14': 15, 'stroop15': 16,
                             'bart3': 17}
            self.DATE = "08/16/23"

            self.amygdala = ["A'1", "A'2", "A'3", "A'4", "A'5", "A'6", "A'7", "A'8", "A'9", "A'10"]
            self.hippocampus_b = ["B'1", "B'2", "B'3", "B'4", "B'5", "B'6", "B'7", "B'8"]
            self.hippocampus_h = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"]
            self.hippocampus_t = ["C'1", "C'2", "C'3", "C'4", "C'5", "C'6", "C'7", "C'8", "C'9", "C'10"]
            self.entorhinal = ["E'1", "E'2", "E'3", "E'4", "E'5", "E'6", "E'7", "E'8"]  # FIXME: CHECK, last two seem irrelevant
            self.para_hippocampus = ["F'1", "F'2", "F'3", "F'4", "F'5", "F'6", "F'7", "F'8", "F'9", "F'10"]
            self.amcc = ["G'1", "G'2", "G'3", "G'4", "G'5", "G'6", "G'7", "G'8", "G'9", "G'10", "G'11", "G'12"]  # corpus callosum
            self.temporal_pole = ["I'1", "I'2", "I'3", "I'4", "I'5", "I'6", "I'7", "I'8"]
            self.gyrus_rectus = ["O'1", "O'2", "O'3", "O'4", "O'5", "O'6", "O'7", "O'8", "O'9", "O'10"]  # also include olfactory and orbital
            self.ant_insula = ["Q'1", "Q'2", "Q'3", "Q'4", "Q'5", "Q'6", "Q'7", "Q'8"]
            self.pos_insula = ["U'1", "U'2", "U'3", "U'4", "U'5", "U'6", "U'7", "U'8"]
            self.ant_cc = ["X'1", "X'2", "X'3", "X'4", "X'5", "X'6", "X'7", "X'8", "X'9", "X'10", "X'11", "X'12"]
            self.ant_insula_l = ["Y'1", "Y'2", "Y'3", "Y'4", "Y'5", "Y'6", "Y'7", "Y'8", "Y'9", "Y'10", "Y'11", "Y'12", "Y'13", "Y'14"]
            self.ant_insula_r = ["Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "Y10", "Y11", "Y12", "Y13", "Y14"]
        elif patient == 'p2':
            self.NUM_STROOP = 8
            self.NUM_BART = 2
            self.E_MAP = {'stroop1': 0, 'bart1': 1, 'stroop2': 2, 'stroop3': 3, 'stroop4': 4, 'bart2': 5,
                             'stroop5': 6, 'stroop6': 7, 'stroop7': 8, 'stroop8': 9}
            self.DATE = "07/17/23"

            self.amygdala = ["A'1", "A'2", "A'3", "A'4", "A'5", "A'6", "A'7", "A'8", "A'9", "A'10"]
            self.ant_hippocampus = ["B'1", "B'2", "B'3", "B'4", "B'5", "B'6", "B'7", "B'8"]
            self.pos_hippocampus = ["C'1", "C'2", "C'3", "C'4", "C'5", "C'6", "C'7", "C'8", "C'9", "C'10"]
            self.entorhinal = ["E'1", "E'2", "E'3", "E'4", "E'5", "E'6", "E'7", "E'8"]
            self.para_hippocampus = ["F'1", "F'2", "F'3", "F'4", "F'5", "F'6", "F'7", "F'8", "F'9", "F'10"]
            self.amcc = ["G'1", "G'2", "G'3", "G'4", "G'5", "G'6", "G'7", "G'8", "G'9", "G'10", "G'11", "G'12"]
            self.gyrus_rectus = ["O'1", "O'2", "O'3", "O'4", "O'5", "O'6", "O'7", "O'8", "O'9", "O'10", "O'11", "O'12"]
            self.precuneus = ["P'1", "P'2", "P'3", "P'4", "P'5", "P'6", "P'7", "P'8", "P'9", "P'10"]
            self.stg = ["T'1", "T'2", "T'3", "T'4"]
            self.heschl = ["U'1", "U'2", "U'3", "U'4", "U'5", "U'6"]
            self.mid_insula = ["X'1", "X'2", "X'3", "X'4", "X'5", "X'6", "X'7", "X'8", "X'9", "X'10", "X'11", "X'12"]
            self.insula = ["Y'1", "Y'2", "Y'3", "Y'4", "Y'5", "Y'6", "Y'7", "Y'8", "Y'9", "Y'10", "Y'11", "Y'12"]
        elif patient == 'p1':
            self.DATE = "06/17/23"
        else:
            raise TypeError(patient + " does not exist")

        self.NUM_EXP = self.NUM_BART + self.NUM_STROOP

