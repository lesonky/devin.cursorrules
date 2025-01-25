#!/usr/bin/env python3
"""
Calendar Tool - 用于创建系统日历事件的工具
"""

import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Optional, List, Tuple

class CalendarTool:
    def __init__(self):
        self.script_template = '''
        try
            tell application "Calendar"
                tell calendar "{calendar}"
                    make new event at end with properties {{summary:"{title}", start date:date "{start_date}", end date:date "{end_date}", description:"{description}", location:"{location}"}}
                end tell
            end tell
            return "success"
        on error errMsg
            return "error: " & errMsg
        end try
        '''

    @staticmethod
    def get_today() -> datetime:
        """获取今天的日期时间"""
        return datetime.now().replace(microsecond=0)

    @staticmethod
    def parse_relative_time(time_str: str) -> Optional[datetime]:
        """
        解析相对时间字符串，如 "today 16:30"
        
        Args:
            time_str: 时间字符串，格式可以是:
                     - "today HH:MM" 表示今天的某个时间
                     - "tomorrow HH:MM" 表示明天的某个时间
                     - 或者标准的 ISO 格式
        
        Returns:
            datetime 对象，如果解析失败则返回 None
        """
        time_str = time_str.lower().strip()
        
        if time_str.startswith(("today", "tomorrow")):
            try:
                base_date = CalendarTool.get_today()
                if time_str.startswith("tomorrow"):
                    base_date += timedelta(days=1)
                    time_part = time_str.replace("tomorrow", "").strip()
                else:
                    time_part = time_str.replace("today", "").strip()
                
                hour, minute = map(int, time_part.split(":"))
                return base_date.replace(hour=hour, minute=minute)
            except (ValueError, TypeError):
                return None
        
        return parse_datetime(time_str)

    def create_event(
        self,
        title: str,
        start_time: datetime,
        end_time: datetime,
        calendar: str = "Home",
        description: str = "",
        location: str = ""
    ) -> bool:
        """
        创建一个新的日历事件
        
        Args:
            title: 事件标题
            start_time: 开始时间
            end_time: 结束时间
            calendar: 目标日历名称
            description: 事件描述
            location: 事件地点
            
        Returns:
            bool: 是否创建成功
        """
        try:
            # 首先检查日历是否存在
            available_calendars = self.list_calendars()
            if calendar not in available_calendars:
                print(f"错误: 找不到日历 '{calendar}'。可用的日历: {', '.join(available_calendars)}", file=sys.stderr)
                return False

            script = self.script_template.format(
                calendar=calendar,
                title=title.replace('"', '\\"'),
                start_date=start_time.strftime("%Y-%m-%d %H:%M:%S"),
                end_date=end_time.strftime("%Y-%m-%d %H:%M:%S"),
                description=description.replace('"', '\\"'),
                location=location.replace('"', '\\"')
            )
            
            print(f"正在创建事件: {title}", file=sys.stderr)
            print(f"日历: {calendar}", file=sys.stderr)
            print(f"时间: {start_time} - {end_time}", file=sys.stderr)
            
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0 or result.stdout.strip().startswith("error:"):
                print(f"创建事件失败: {result.stderr or result.stdout}", file=sys.stderr)
                return False
                
            return True
            
        except Exception as e:
            print(f"发生错误: {str(e)}", file=sys.stderr)
            return False

    def list_calendars(self) -> List[str]:
        """
        获取系统中所有可用的日历列表
        
        Returns:
            List[str]: 日历名称列表
        """
        script = '''
        try
            tell application "Calendar"
                get name of calendars
            end tell
        on error errMsg
            return "error: " & errMsg
        end try
        '''
        
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0 or result.stdout.strip().startswith("error:"):
                print(f"获取日历列表失败: {result.stderr or result.stdout}", file=sys.stderr)
                return []
                
            # 处理返回的日历列表
            output = result.stdout.strip()
            if not output:
                return []
                
            # 移除可能的引号并分割
            calendars = [cal.strip(' "') for cal in output.split(",")]
            return [cal for cal in calendars if cal]  # 移除空值
            
        except Exception as e:
            print(f"发生错误: {str(e)}", file=sys.stderr)
            return []

def parse_datetime(dt_str: str) -> datetime:
    """解析日期时间字符串"""
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        try:
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("无效的日期时间格式。请使用 ISO 格式 (YYYY-MM-DDTHH:MM:SS) 或 'YYYY-MM-DD HH:MM:SS'")

def main():
    parser = argparse.ArgumentParser(description="创建系统日历事件")
    parser.add_argument("--list-calendars", action="store_true", help="列出所有可用的日历")
    
    # 创建事件相关的参数组
    event_group = parser.add_argument_group("event", "事件相关参数")
    event_group.add_argument("--title", help="事件标题")
    event_group.add_argument(
        "--start",
        help="开始时间。可以是以下格式:\n"
             "- YYYY-MM-DDTHH:MM:SS (ISO格式)\n"
             "- YYYY-MM-DD HH:MM:SS\n"
             "- today HH:MM (今天的某个时间)\n"
             "- tomorrow HH:MM (明天的某个时间)"
    )
    event_group.add_argument(
        "--end",
        help="结束时间。格式同 --start"
    )
    event_group.add_argument("--calendar", default="Home", help="目标日历名称")
    event_group.add_argument("--description", default="", help="事件描述")
    event_group.add_argument("--location", default="", help="事件地点")
    
    args = parser.parse_args()
    
    tool = CalendarTool()
    
    if args.list_calendars:
        calendars = tool.list_calendars()
        if calendars:
            print("可用的日历:")
            for cal in calendars:
                print(f"- {cal}")
        else:
            print("未找到可用的日历", file=sys.stderr)
            sys.exit(1)
        return
    
    # 检查创建事件所需的必要参数
    if not all([args.title, args.start, args.end]):
        if not args.list_calendars:  # 只有在不是列出日历的情况下才报错
            parser.error("创建事件需要提供 --title, --start 和 --end 参数")
        return
    
    try:
        # 解析开始和结束时间
        start_time = tool.parse_relative_time(args.start)
        if not start_time:
            raise ValueError(f"无法解析开始时间: {args.start}")
            
        end_time = tool.parse_relative_time(args.end)
        if not end_time:
            raise ValueError(f"无法解析结束时间: {args.end}")
        
        success = tool.create_event(
            title=args.title,
            start_time=start_time,
            end_time=end_time,
            calendar=args.calendar,
            description=args.description,
            location=args.location
        )
        
        if success:
            print("事件创建成功")
        else:
            print("事件创建失败", file=sys.stderr)
            sys.exit(1)
            
    except ValueError as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 