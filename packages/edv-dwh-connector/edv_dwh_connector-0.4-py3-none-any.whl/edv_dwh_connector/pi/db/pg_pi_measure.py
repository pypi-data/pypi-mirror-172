"""
This module implements PI tag API coming from PostgreSQL.
.. since: 0.2
"""

# -*- coding: utf-8 -*-
# Copyright (c) 2022 Endeavour Mining
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to read
# the Software only. Permissions is hereby NOT GRANTED to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime

from sqlalchemy import text  # type: ignore
from edv_dwh_connector.pi.pi_measure import PIMeasure, PIMeasures
from edv_dwh_connector.pi.pi_tag import PITag
from edv_dwh_connector.dwh import Dwh
from edv_dwh_connector.exceptions import ValueNotFoundError,\
    ValueAlreadyExistsError

# pylint: disable=line-too-long


class PgPIMeasure(PIMeasure):
    """
    PI measure from PostgreSQL.
    .. since: 0.2
    """

    def __init__(self, tag: PITag, date: datetime, dwh: Dwh) -> None:
        """
        Ctor.
        :param tag: PI tag
        :param date: Datetime
        :param dwh: Data warehouse
        :raises ValueNotFoundError: If not found
        """
        self.__tag = tag
        self.__date = datetime.strptime(
            date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "%Y-%m-%d %H:%M:%S.%f"
        )
        with dwh.connection() as conn:
            row = conn.execute(
                text(
                    "SELECT value "
                    "FROM v_pi_measure "
                    "WHERE code = :code"
                    " and full_datetime = :date"
                ),
                (
                    {
                        "code": self.__tag.code(),
                        "date": self.__date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # noqa: E501
                    }
                )
            ).fetchone()
            if row is None:
                raise ValueNotFoundError("PI measure not found")
            self.__value = row["value"]

    def tag(self) -> PITag:
        return self.__tag

    def date(self) -> datetime:
        return self.__date

    def value(self) -> float:
        return float(self.__value)


class PgPIMeasures(PIMeasures):
    """
    PI measures from PostgreSQL.
    .. since: 0.2
    """

    def __init__(self, tag: PITag, dwh: Dwh):
        """
        Ctor.
        :param tag: Tag
        :param dwh: Data warehouse
        """
        self.__tag = tag
        self.__dwh = dwh

    def has_at(self, date: datetime) -> bool:
        has = True
        try:
            PgPIMeasure(self.__tag, date, self.__dwh)
        except ValueNotFoundError:
            has = False
        return has

    def items(self, start: datetime, end: datetime) -> list:
        result = []
        with self.__dwh.connection() as conn:
            for row in conn.execute(
                text(
                    "SELECT TO_TIMESTAMP(full_datetime, 'YYYY-MM-DD HH24:MI:SS.MS') FROM v_pi_measure "  # noqa: E501
                    "WHERE full_datetime "
                    "BETWEEN :start AND :end "
                    "AND code = :code"
                ),
                (
                    {
                        "start": start.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                        "end": end.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                        "code": self.__tag.code()
                    }
                )
            ).fetchall():
                result.append(
                    PgPIMeasure(self.__tag, row[0], self.__dwh)
                )
        return result

    def add(self, date: datetime, value: float) -> PIMeasure:
        if self.has_at(date):
            raise ValueAlreadyExistsError(
                "A measure already exists at "
                f"{date} for tag {self.__tag.code()}"
            )
        with self.__dwh.connection() as conn:
            conn.execute(
                text(
                    "INSERT INTO fact_pi_measure "
                    "(tag_pk, date_pk, time_pk, value, millisecond) "
                    "VALUES"
                    "(:tag_pk, :date_pk, :time_pk, :value, :millis) "
                ),
                (
                    {
                        "tag_pk": self.__tag.uid(),
                        "date_pk": self.__date_pk(date),
                        "time_pk": self.__time_pk(date),
                        "value": value,
                        "millis": int(date.microsecond / 1000)
                    }
                )
            )
            return PgPIMeasure(
                self.__tag, date, self.__dwh
            )

    def __date_pk(self, date: datetime) -> int:
        """
        Date key.
        :param date: Datetime
        :return: UID
        :raises ValueNotFoundError: If key not found
        """
        with self.__dwh.connection() as conn:
            uid, = conn.execute(
                text(
                    "SELECT date_pk FROM dim_date "
                    "WHERE date_value = :date "
                ),
                ({"date": date.date()})
            ).fetchone()
            if uid is None:
                raise ValueNotFoundError("Saving PI measure: Date not found")
            return uid

    def __time_pk(self, date: datetime) -> int:
        """
        Time key.
        :param date: Datetime
        :return: UID
        :raises ValueNotFoundError: If key not found
        """
        with self.__dwh.connection() as conn:
            row = conn.execute(
                text(
                    "SELECT time_pk FROM dim_time "
                    "WHERE time_value = :time"
                ),
                ({"time": date.time().strftime("%H:%M:%S")})
            ).fetchone()
            if row is None:
                raise ValueNotFoundError("Saving PI measure: Time not found")
            return row["time_pk"]
