from svgdiagram.elements.svg import Svg
from svgdiagram.elements.group import Group
from svgdiagram.elements.text import Text
from svgdiagram.elements.path import Path
from svgdiagram.elements.rect import Rect
from datetime import datetime, timedelta, date
from svgdiagram.derived_elements.multi_line_rect import MultiLineRect, TextLine

from .gantt_content import GanttContent
from .gantt_options import GanttOptions
from .utils import day_iterator
from .swimlane import CalendarSwimlane

from svgdiagram.shapes.connection import Connection, ShapeConnectType
from svgdiagram.elements.marker import MarkerArrow

from .renderer.swimlane import render_swimlane


DEFAULT_STYLING = {
    "CALENDAR": {
        "STYLE": "DAY",  # DAY, WEEK, MONTH, AUTO
        "DAY_WIDTH": 50.0,
        "DAY_FONT": {
            "SIZE": 16.0
        },
        "DAY_COLUMN_COLOR": "#bbbbbb",
        "DAY_COLUMN_COLOR_ODD": "#dddddd",
    }
}
DEFAULT_OPTIONS = {
    "DATE_DEFAULT_TIME": "T12:00:00"
}


class Gantt(Svg):
    def __init__(self, content, style=None, options=None):
        super().__init__()

        self.content = GanttContent.parse_obj(content)
        self.style = style if style else DEFAULT_STYLING
        self.options = options if options else GanttOptions()

        self.group_calendar_tiles = Group()
        self.append_child(self.group_calendar_tiles)
        self.group_calendar_text = Group()
        self.append_child(self.group_calendar_text)

        self.group_swimlanes = Group()
        self.append_child(self.group_swimlanes)

        self.group_dependencies = Group()
        self.append_child(self.group_dependencies)

        self.id_shape_map = {}

    @property
    def start_date(self):
        if not self.content.start_date:
            min_date = min(self.content.iter_all_swimlane_dates())
            if isinstance(min_date, datetime):
                min_date = min_date.date()
            self.content.start_date = min_date
        return self.content.start_date

    @property
    def end_date(self):
        if not self.content.end_date:
            max_date = max(self.content.iter_all_swimlane_dates())
            if isinstance(max_date, datetime):
                max_date = max_date.date()
            self.content.end_date = max_date
        return self.content.end_date

    @property
    def calendar_x_min(self):
        DAY_WIDTH = self.style["CALENDAR"]["DAY_WIDTH"]
        return self.date_to_column_index(
            self.start_date) * DAY_WIDTH

    @property
    def calendar_x_max(self):
        DAY_WIDTH = self.style["CALENDAR"]["DAY_WIDTH"]
        return (self.date_to_column_index(
            self.end_date) + 1) * DAY_WIDTH

    @property
    def calendar_width(self):
        return self.calendar_x_max - self.calendar_x_min

    def date_to_column_index(self, date_value):
        """Gives the correct column index based on a date"""

        if isinstance(date_value, datetime):
            date_value = date_value.date()

        assert isinstance(date_value, date), \
            f'"{date_value}" is not a datetime.date!'

        return (date_value - self.start_date).days

    def date_to_column_fraction(self, datetime_value):
        """Gives the correct column index and the fraction within it based on a datetime."""

        if type(datetime_value) == date:
            datetimestr = datetime_value.isoformat() \
                + "T" + self.options.date_default_time.isoformat()
            datetime_value = datetime.fromisoformat(datetimestr)

        assert isinstance(datetime_value, datetime), \
            f'"{datetime_value}" is not a datetime.datetime!'

        index = self.date_to_column_index(datetime_value)

        seconds_of_day = datetime_value.second \
            + datetime_value.minute * 60 \
            + datetime_value.hour * 3600
        fraction = seconds_of_day / float(24 * 3600)

        return index, fraction

    def date_to_column_x_pos(self, datetime_value):
        DAY_WIDTH = self.style["CALENDAR"]["DAY_WIDTH"]
        index, fraction = self.date_to_column_fraction(datetime_value)
        return (index + fraction) * DAY_WIDTH

    def _layout(self, x_con_min, x_con_max, y_con_min, y_con_max):
        assert self.start_date <= self.end_date, \
            f'Enddate "{self.end_date}" is before startdate "{self.start_date}"!'

        if not any(map(lambda x: isinstance(x, CalendarSwimlane), self.content.swimlanes)):
            self.content.swimlanes.insert(0, CalendarSwimlane(
                show_years=True,
                show_months=True,
                show_weeks=True,
                show_days=True,
            ))

        y_offset = 0
        swimlane_y_max = self._build_swimlanes(y_offset)
        self._build_calender_tiles(swimlane_y_max)

        for dep in self.content.dependencies:
            connection = Connection(
                start_point=self.id_shape_map[dep.source_id],
                end_point=self.id_shape_map[dep.target_id],
                start_shape_connect_type=ShapeConnectType.CLOSEST,
                end_shape_connect_type=ShapeConnectType.CLOSEST,
                normal_len=20,
            )

            path = Path(connection.calculate_points(),
                        corner_radius=10, marker_end=MarkerArrow())
            self.group_dependencies.append_child(path)

        super()._layout(x_con_min, x_con_max, y_con_min, y_con_max)

    def _build_calendar_years(self, y_offset, show_years):
        if not show_years:
            return y_offset

        DAY_WIDTH = self.style["CALENDAR"]["DAY_WIDTH"]
        DAY_FONT_SIZE = self.style["CALENDAR"]["DAY_FONT"]["SIZE"]
        year_font_size = DAY_FONT_SIZE*2

        first_entry_index = None

        for c_date in day_iterator(self.start_date, self.end_date):

            index = self.date_to_column_index(c_date)

            if (c_date.day == 1 and c_date.month == 1):
                first_entry_index = index
                self.group_calendar_text.append_child(
                    Text(index * DAY_WIDTH + 5, y_offset+year_font_size,
                         c_date.strftime('%Y'), horizontal_alignment="left", font_size=year_font_size)
                )

        if first_entry_index is None:
            self.group_calendar_text.append_child(
                Text(5, y_offset+year_font_size,
                     self.start_date.strftime('%Y'), horizontal_alignment="left", font_size=year_font_size)
            )

        self.group_calendar_text.insert_child(
            0,
            Rect(self.calendar_x_min, y_offset,
                 self.calendar_width, year_font_size*2,
                 stroke="transparent", fill="#FFFFFFEE")
        )

        self.group_calendar_text.append_child(
            Path([(self.calendar_x_min, y_offset),
                 (self.calendar_x_max, y_offset)])
        )

        return y_offset + 2 * year_font_size

    def _build_calendar_months(self, y_offset, show_months):
        if not show_months:
            return y_offset

        DAY_WIDTH = self.style["CALENDAR"]["DAY_WIDTH"]
        DAY_FONT_SIZE = self.style["CALENDAR"]["DAY_FONT"]["SIZE"]
        month_font_size = DAY_FONT_SIZE

        first_entry_index = None

        for c_date in day_iterator(self.start_date, self.end_date):
            index = self.date_to_column_index(c_date)

            if c_date.day == 1:
                first_entry_index = index
                self.group_calendar_text.append_child(
                    Text(index * DAY_WIDTH + 5, y_offset+month_font_size,
                         c_date.strftime('%B').upper(), horizontal_alignment="left")
                )

        if first_entry_index is None:
            self.group_calendar_text.append_child(
                Text(5, y_offset+month_font_size,
                     self.start_date.strftime('%B').upper(), horizontal_alignment="left")
            )

        # background_month
        self.group_calendar_text.insert_child(
            0,
            Rect(self.calendar_x_min, y_offset,
                 self.calendar_width, month_font_size*2,
                 stroke="transparent", fill="#FFFFFFDD")
        )

        self.group_calendar_text.append_child(
            Path([(self.calendar_x_min, y_offset),
                 (self.calendar_x_max, y_offset)])
        )

        return y_offset + month_font_size*2

    def _build_calendar_weeks(self, y_offset, show_weeks):
        if not show_weeks:
            return y_offset

        DAY_WIDTH = self.style["CALENDAR"]["DAY_WIDTH"]
        DAY_FONT_SIZE = self.style["CALENDAR"]["DAY_FONT"]["SIZE"]
        week_font_size = DAY_FONT_SIZE

        first_entry_index = None

        for c_date in day_iterator(self.start_date, self.end_date):
            index = self.date_to_column_index(c_date)
            year, week, weekday = c_date.isocalendar()

            if weekday == 1:
                first_entry_index = index
                self.group_calendar_text.append_child(
                    Text(index * DAY_WIDTH + 5, y_offset + week_font_size,
                         f"CW {week}", horizontal_alignment="left", font_size=week_font_size)
                )
                self.group_calendar_text.append_child(
                    Path([(index * DAY_WIDTH, y_offset),
                         (index * DAY_WIDTH, y_offset+week_font_size*2)])
                )

        if first_entry_index is None:
            _, start_week, _ = self.start_date.isocalendar()
            self.group_calendar_text.append_child(
                Text(5, y_offset+week_font_size,
                     f"CW {start_week}", horizontal_alignment="left")
            )

        # background_week
        self.group_calendar_text.insert_child(
            0,
            Rect(self.calendar_x_min, y_offset,
                 self.calendar_width, week_font_size*2,
                 stroke="transparent", fill="#FFFFFFAA")
        )

        self.group_calendar_text.append_child(
            Path([(self.calendar_x_min, y_offset),
                 (self.calendar_x_max, y_offset)])
        )

        return y_offset + week_font_size*2

    def _build_calendar_days(self, y_offset, show_days):
        if not show_days:
            return y_offset

        DAY_WIDTH = self.style["CALENDAR"]["DAY_WIDTH"]

        for c_date in day_iterator(self.start_date, self.end_date):
            index = self.date_to_column_index(c_date)

            ml_rect = MultiLineRect(index*DAY_WIDTH, y_offset, DAY_WIDTH, text_lines=[
                TextLine(c_date.strftime(r'%a')),
                TextLine(c_date.strftime(r'%d')),
            ],
                fill="#FFFFFF88"
            )

            self.group_calendar_text.append_child(
                ml_rect
            )

        return y_offset + ml_rect.height

    def _build_calendar(self, y_offset, calendar_swimlane):

        y_offset = self._build_calendar_years(
            y_offset, calendar_swimlane.show_years)
        y_offset = self._build_calendar_months(
            y_offset, calendar_swimlane.show_months)
        y_offset = self._build_calendar_weeks(
            y_offset, calendar_swimlane.show_weeks)
        y_offset = self._build_calendar_days(
            y_offset, calendar_swimlane.show_days)

        return y_offset

    def _build_swimlanes(self, y_offset):
        for swimlane in self.content.swimlanes:
            if isinstance(swimlane, CalendarSwimlane):
                y_offset = self._build_calendar(y_offset, swimlane)
            else:
                y_offset, _group, _id_shape_map = render_swimlane(
                    y_offset,
                    swimlane,
                    xmin=self.calendar_x_min,
                    xmax=self.calendar_x_max,
                    date_to_column_x_pos=self.date_to_column_x_pos,
                )
                self.group_swimlanes.append_child(_group)
                self.id_shape_map.update(_id_shape_map)

        return y_offset

    def _build_calender_tiles(self, swimlane_y_max):
        DAY_WIDTH = self.style["CALENDAR"]["DAY_WIDTH"]
        DAY_COLUMN_COLOR = self.style["CALENDAR"]["DAY_COLUMN_COLOR"]
        DAY_COLUMN_COLOR_ODD = self.style["CALENDAR"]["DAY_COLUMN_COLOR_ODD"]

        c_date = self.start_date
        while c_date <= self.end_date:
            year, week, weekday = c_date.isocalendar()

            index, fraction = self.date_to_column_fraction(c_date)

            day_x = index * DAY_WIDTH
            day_y = 0

            day_color = DAY_COLUMN_COLOR if (
                index % 2) == 0 else DAY_COLUMN_COLOR_ODD

            if weekday > 5:
                day_color = '#ffeb3b'

            if c_date in self.options.public_holidays:
                day_color = '#ff4337'

            self.group_calendar_tiles.append_child(Rect(
                x=day_x,
                y=day_y,
                width=DAY_WIDTH,
                height=swimlane_y_max,
                rx=0, ry=0,
                stroke=day_color,
                stroke_width_px=0,
                fill=day_color,
            ))

            # iter
            c_date += timedelta(days=1)
