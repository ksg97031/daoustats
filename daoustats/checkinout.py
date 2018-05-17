# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import os
import datetime
import numpy as np
import pandas as pd
from glob import glob

import daoustats.settings as settings


class Stats(object):
    def __init__(self):
        self.mdf = None  # Data Frame
        self.mdf = self.__merge()
        self.mdf = self.__filter(self.mdf)

    @property
    def data_frame(self):
        return self.mdf

    def __get_all_data(self):
        """ 데이터 디렉터리에 있는 모든 체크인 데이터 파일들을(*.xlsx) 데이터 프레임 객체로 반환합니다. """
        data_files = glob(str(settings.DATA_DIR.joinpath('*.xlsx')))
        assert len(data_files) > 0, '다우오피스에서 체크인 기록을 받아 "{DATA_DIR}" 경로에 넣어주세요.'.format(
                       DATA_DIR=settings.DATA_DIR)

        for data_file in data_files:
            sheet_columns = ["날짜", "출근", "상태", "퇴근", "근무시간"]
            df = pd.read_excel(data_file, encoding='UTF-8')
            assert all(df.columns.isin(sheet_columns)), '올바르지 않은 형식의 데이터 파일 "{FILE_PATH}"이 존재합니다.'.format(
                           FILE_PATH=data_file)
            yield df

    def __filter(self, df):
        """ 올바른 프로파일링을 위해 불필요한 데이터를 필터하는 함수입니다."""
        now = datetime.datetime.now()
        now_date = now.strftime('%Y-%m-%d')

        df = df[(df['날짜'] <= now_date)]
        df = df[pd.DatetimeIndex(df["날짜"]).weekday < 5]  # 평일 기록만을 가져옵니다.
        df = df[df['출근'].notnull() | df['퇴근'].notnull() | df['상태'].notnull()]  # 공휴일을 제외시킵니다.

        """ 빠진 데이터들을 다듬어서 출력 결과를 더 좋게 포장합니다. """
        df['상태'].fillna('정상 출근', inplace=True)
        df['근무시간'].fillna('09:00:00', inplace=True)  # 체크아웃을 실수로 못한 경우, 기본 근무시간을 할당합니다.

        """ 평균 근무 시간을 계산하기 위해서 새 컬럼을 추가합니다."""
        timestamp_key = '근무시간 - 타임스탬프'
        df[timestamp_key] = (pd.DatetimeIndex(df['근무시간']).astype(np.int64) // 10**9)

        """ 지각 빈도를 알기 위해서 새 컬럼을 추가합니다. """
        df['지각'] = (df['출근'] > '09:00:00') 

        return df

    def __merge(self):
        """ DaouOffice에서는 모든 체크인 기록을 달(Month)별로만 제공하기 때문에 따로 데이터들을 병합해야만 합니다. """
        frames = [x for x in self.__get_all_data()]
        df = pd.concat(frames)
        return df

    def to_file(self, filename):
        """ 가공된 데이터 프레임 객체를 파일로 만듭니다. """
        self.mdf.to_excel(filename)
