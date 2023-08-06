# Copyright (c) 2022 Zhendong Peng (pzd17@tsinghua.org.cn)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from tn.processor import Processor
from tn.chinese.rules.cardinal import Cardinal
from tn.chinese.rules.char import Char
from tn.chinese.rules.date import Date
from tn.chinese.rules.fraction import Fraction
from tn.chinese.rules.math import Math
from tn.chinese.rules.measure import Measure
from tn.chinese.rules.money import Money
from tn.chinese.rules.postprocessor import PostProcessor
from tn.chinese.rules.preprocessor import PreProcessor
from tn.chinese.rules.sport import Sport
from tn.chinese.rules.time import Time
from tn.chinese.rules.whitelist import Whitelist

from pynini import Far
from pynini.lib.pynutil import add_weight, delete, insert
from importlib_resources import files


class Normalizer(Processor):

    def __init__(self,
                 cache_dir=None,
                 overwrite_cache=False,
                 remove_interjections=True,
                 full_to_half=True,
                 remove_puncts=False,
                 tag_oov=False):
        super().__init__(name='normalizer')
        self.cache_dir = cache_dir
        self.overwrite_cache = overwrite_cache
        self.remove_interjections = remove_interjections
        self.full_to_half = full_to_half
        self.remove_puncts = remove_puncts
        self.tag_oov = tag_oov

        far_file = files('tn').joinpath('zh_tn_normalizer.far')
        if self.cache_dir:
            os.makedirs(self.cache_dir, exist_ok=True)
            far_file = os.path.join(self.cache_dir, 'zh_tn_normalizer.far')

        if far_file and os.path.exists(far_file) and not overwrite_cache:
            self.tagger = Far(far_file)['tagger']
            self.verbalizer = Far(far_file)['verbalizer']
        else:
            self.build_tagger()
            self.build_verbalizer()

        if self.cache_dir and self.overwrite_cache:
            self.export(far_file)

    def build_tagger(self):
        cardinal = Cardinal().tagger
        char = Char().tagger
        date = Date().tagger
        fraction = Fraction().tagger
        math = Math().tagger
        measure = Measure().tagger
        money = Money().tagger
        sport = Sport().tagger
        time = Time().tagger
        whitelist = Whitelist().tagger

        to = (delete('-') | delete('~')) + insert(' char { value: "到" } ')
        date = date + (to + date).ques
        time = time + (to + time).ques

        tagger = (add_weight(date, 1.02)
                  | add_weight(whitelist, 1.03)
                  | add_weight(sport, 1.04)
                  | add_weight(fraction, 1.05)
                  | add_weight(measure, 1.05)
                  | add_weight(money, 1.05)
                  | add_weight(time, 1.05)
                  | add_weight(cardinal, 1.06)
                  | add_weight(math, 1.08)
                  | add_weight(char, 100)).optimize().star
        # delete the last space
        tagger @= self.build_rule(delete(' '), r='[EOS]')

        processor = PreProcessor(
            remove_interjections=self.remove_interjections,
            full_to_half=self.full_to_half).processor
        self.tagger = processor @ tagger.optimize()

    def build_verbalizer(self):
        cardinal = Cardinal().verbalizer
        char = Char().verbalizer
        date = Date().verbalizer
        fraction = Fraction().verbalizer
        math = Math().verbalizer
        measure = Measure().verbalizer
        money = Money().verbalizer
        sport = Sport().verbalizer
        time = Time().verbalizer
        whitelist = Whitelist().verbalizer

        verbalizer = (cardinal | char | date | fraction | math | measure
                      | money | sport | time | whitelist).optimize().star

        processor = PostProcessor(remove_puncts=self.remove_puncts,
                                  tag_oov=self.tag_oov).processor
        self.verbalizer = verbalizer @ processor
