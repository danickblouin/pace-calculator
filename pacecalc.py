#!/usr/bin/env python3
"""
Pace Calculator - A beautiful, feature-rich tool for runners
Calculates pace, time, and distance with colored output and additional insights
"""

import argparse
import re
import sys
from typing import Tuple, Dict, Any
from dataclasses import dataclass
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

@dataclass
class RunningMetrics:
    """Container for running metrics and calculations"""
    distance_km: float
    time_minutes: float
    pace_min_per_km: float
    speed_kmh: float
    splits: Dict[str, str]
    projected_times: Dict[str, str]
    training_zones: Dict[str, str]

class InputError(Exception):
    """Custom exception for invalid input"""
    def __init__(self, unit: str, input_type: str):
        self.unit = unit
        self.input_type = input_type
        super().__init__(f"'{unit}' is not a valid input for {input_type}")

class PaceCalculator:
    """Pace calculator with additional features"""
    
    # Distance units and conversions
    DISTANCE_UNITS = {
        "mi": 1.609344,
        "km": 1.0,
        "k": 1.0,
        "m": 42.195,  # marathon
        "marathon": 42.195,
        "hm": 21.0975,  # half-marathon
        "half-marathon": 21.0975,
        "10k": 10.0,
        "5k": 5.0,
        "1k": 1.0,
        "400m": 0.4,
        "800m": 0.8,
        "1mi": 1.609344,
    }
    
    # Training zones based on pace (simplified)
    TRAINING_ZONES = {
        "Easy": (1.15, 1.25),       # 115–125% of threshold pace 
        "Threshold": (1.05, 1.15),  # 105–115% of threshold pace
        "Tempo": (1.0, 1.05),       # 100–105% of threshold pace
        "VO2 Max": (0.9, 1.0),      # 90–100% of threshold pace
        "Speed": (0.8, 0.9)         # 80–90% of threshold pace
    }
    
    def __init__(self):
        self.colors = {
            "title": Fore.CYAN + Style.BRIGHT,
            "success": Fore.GREEN + Style.BRIGHT,
            "info": Fore.BLUE,
            "warning": Fore.YELLOW,
            "error": Fore.RED + Style.BRIGHT,
            "highlight": Fore.MAGENTA + Style.BRIGHT,
            "reset": Style.RESET_ALL
        }
    
    def print_banner(self):
        banner = f"""
{self.colors['title']}+===============================================================+
|                        PACE CALCULATOR                        |
+===============================================================+{self.colors['reset']}
"""
        print(banner)
    
    def distance_str_to_km(self, distance: str) -> float:
        """Convert distance string to kilometers"""
        distance = distance.lower().strip()
        
        # Check for preset distances first
        if distance in self.DISTANCE_UNITS:
            return self.DISTANCE_UNITS[distance]
        
        # Check for units
        for unit, multiplier in self.DISTANCE_UNITS.items():
            if distance.endswith(unit):
                try:
                    value = distance.removesuffix(unit)
                    return float(value) * multiplier
                except ValueError:
                    raise InputError(distance, "distance")
        
        # Try as plain number (assume km)
        try:
            return float(distance)
        except ValueError:
            raise InputError(distance, "distance")
    
    def time_str_to_minutes(self, time: str) -> float:
        """Convert time string to minutes"""
        time = time.strip()
        
        # Check for letter-based format (e.g., 1h30m20s)
        if any(x in time for x in "hms"):
            return self._parse_time_with_letters(time)
        
        # Check for colon-based format (e.g., 1:30:45)
        if ":" in time:
            return self._parse_time_with_colons(time)
        
        # Try as plain number (assume minutes)
        try:
            return float(time)
        except ValueError:
            raise InputError(time, "time")
    
    def _parse_time_with_letters(self, time: str) -> float:
        """Parse time in format like 1h30m20s"""
        pattern = r"^(?:(?P<hours>\d+(?:\.\d+)?)h)?(?:(?P<minutes>\d+(?:\.\d+)?)m)?(?:(?P<seconds>\d+)s)?$"
        match = re.match(pattern, time)
        
        if not match:
            raise InputError(time, "time")
        
        hours = float(match.group("hours") or 0)
        minutes = float(match.group("minutes") or 0)
        seconds = float(match.group("seconds") or 0)
        
        return hours * 60 + minutes + seconds / 60
    
    def _parse_time_with_colons(self, time: str) -> float:
        """Parse time in format like 1:30:45"""
        parts = time.split(":")
        
        if len(parts) == 2:  # M:S format
            minutes, seconds = parts
            return float(minutes) + float(seconds) / 60
        elif len(parts) == 3:  # H:M:S format
            hours, minutes, seconds = parts
            return float(hours) * 60 + float(minutes) + float(seconds) / 60
        else:
            raise InputError(time, "time")
    
    def pace_str_to_minutes(self, pace: str) -> float:
        """Convert pace string to minutes per km"""
        pace = pace.strip()
        
        # Check for colon format (e.g., 4:30)
        if ":" in pace:
            parts = pace.split(":")
            if len(parts) == 2:
                minutes, seconds = parts
                return float(minutes) + float(seconds) / 60
        
        # Try as plain number (assume minutes)
        try:
            return float(pace)
        except ValueError:
            raise InputError(pace, "pace")
    
    def minutes_to_time_str(self, minutes: float, show_hours: bool = True) -> str:
        """Convert minutes to formatted time string"""
        if minutes < 60 or not show_hours:
            mins, secs = divmod(minutes, 1)
            return f"{int(mins)}:{int(secs * 60):02d}"
        
        hours, remaining_minutes = divmod(minutes, 60)
        mins, secs = divmod(remaining_minutes, 1)
        return f"{int(hours)}:{int(mins):02d}:{int(secs * 60):02d}"
    
    def calculate_metrics(self, distance: str = None, time: str = None, pace: str = None) -> RunningMetrics:
        """Calculate all running metrics from two given values"""
        if distance and time and not pace:
            # Calculate pace
            dist_km = self.distance_str_to_km(distance)
            time_mins = self.time_str_to_minutes(time)
            pace_mins = time_mins / dist_km
        elif distance and pace and not time:
            # Calculate time
            dist_km = self.distance_str_to_km(distance)
            pace_mins = self.pace_str_to_minutes(pace)
            time_mins = dist_km * pace_mins
        elif time and pace and not distance:
            # Calculate distance
            time_mins = self.time_str_to_minutes(time)
            pace_mins = self.pace_str_to_minutes(pace)
            dist_km = time_mins / pace_mins
        else:
            raise ValueError("Exactly two of distance, time, and pace must be provided")
        
        # Calculate derived metrics
        speed_kmh = 60 / pace_mins if pace_mins > 0 else 0
        
        # Calculate splits for common distances
        splits = self._calculate_splits(pace_mins)
        
        # Calculate projected times for common distances
        projected_times = self._calculate_projected_times(dist_km, time_mins, pace_mins)
        
        # Calculate training zones
        training_zones = self._calculate_training_zones(pace_mins)
        
        return RunningMetrics(
            distance_km=dist_km,
            time_minutes=time_mins,
            pace_min_per_km=pace_mins,
            speed_kmh=speed_kmh,
            splits=splits,
            projected_times=projected_times,
            training_zones=training_zones
        )
    
    def _calculate_splits(self, pace_mins: float) -> Dict[str, str]:
        """Calculate splits for common distances"""
        common_distances = [1, 5, 10, 21.0975, 42.195]
        splits = {}
        
        for dist in common_distances:
            time_mins = dist * pace_mins
            splits[f"{dist}km"] = self.minutes_to_time_str(time_mins, dist >= 10)
        
        return splits
    
    def _calculate_projected_times(self, distance_km: float, time_mins: float, pace_mins: float) -> Dict[str, str]:
        """Calculate projected times for common distances"""
        common_distances = [5, 10, 21.0975, 42.195]
        projected = {}
        
        for dist in common_distances:
            if dist != distance_km:
                time_mins = dist * pace_mins
                projected[f"{dist}km"] = self.minutes_to_time_str(time_mins, dist >= 10)
        
        return projected
    
    def _calculate_training_zones(self, threshold_pace: float) -> Dict[str, str]:
        """Calculate training zones based on threshold pace"""
        zones = {}
        
        for zone_name, (min_mult, max_mult) in self.TRAINING_ZONES.items():
            min_pace = threshold_pace * min_mult
            max_pace = threshold_pace * max_mult
            zones[zone_name] = f"{self.minutes_to_time_str(min_pace, False)} - {self.minutes_to_time_str(max_pace, False)}"
        
        return zones
    
    def _is_likely_time(self, value: str) -> bool:
        """Determine if a value is likely a time input"""
        value = value.strip().lower()
        
        # Check for preset distances first (these are never times)
        if value in self.DISTANCE_UNITS:
            return False
        
        # Check for time indicators
        if any(x in value for x in "hms:"):
            return True
        
        # Check for colon format (time)
        if ":" in value:
            return True
        
        # If it's just a number, assume it's not time (could be distance or pace)
        try:
            float(value)
            return False
        except ValueError:
            return False
    
    def display_results(self, metrics: RunningMetrics, input_distance: str = None, input_time: str = None, input_pace: str = None):
        """Display results in a beautiful, colored format"""
        print(f"\n{self.colors['success']}🎯 CALCULATION RESULTS{self.colors['reset']}")
        print("=" * 50)
        
        # Main results
        print(f"\n{self.colors['highlight']}📊 MAIN METRICS:{self.colors['reset']}")
        print(f"  Distance: {self.colors['info']}{metrics.distance_km:.3f} km{self.colors['reset']}")
        print(f"  Time:     {self.colors['info']}{self.minutes_to_time_str(metrics.time_minutes, True)}{self.colors['reset']}")
        print(f"  Pace:     {self.colors['info']}{self.minutes_to_time_str(metrics.pace_min_per_km, False)} min/km{self.colors['reset']}")
        print(f"  Speed:    {self.colors['info']}{metrics.speed_kmh:.1f} km/h{self.colors['reset']}")
        
        # Splits
        print(f"\n{self.colors['highlight']}⏱️  SPLITS:{self.colors['reset']}")
        for distance, time in metrics.splits.items():
            print(f"  {distance:>6}: {self.colors['info']}{time}{self.colors['reset']}")
        
        # Projected times
        if metrics.projected_times:
            print(f"\n{self.colors['highlight']}🔮 PROJECTED TIMES:{self.colors['reset']}")
            for distance, time in metrics.projected_times.items():
                print(f"  {distance:>6}: {self.colors['info']}{time}{self.colors['reset']}")
        
        # Training zones
        print(f"\n{self.colors['highlight']}🏃‍♂️ TRAINING ZONES (based on current pace):{self.colors['reset']}")
        for zone, pace_range in metrics.training_zones.items():
            print(f"  {zone:>10}: {self.colors['info']}{pace_range} min/km{self.colors['reset']}")
        
        # Performance insights
        print(f"\n{self.colors['highlight']}💡 PERFORMANCE INSIGHTS:{self.colors['reset']}")
        self._display_performance_insights(metrics)
        
        print("\n" + "=" * 50)
    
    def _display_performance_insights(self, metrics: RunningMetrics):
        """Display performance insights and recommendations"""
        pace = metrics.pace_min_per_km
        
        if pace <= 3:  # 3:00 min/km or faster
            print(f"  {self.colors['success']}🚀 Elite level performance! You're in the top tier of runners.{self.colors['reset']}")
        elif pace <= 4:  # 4:00 min/km
            print(f"  {self.colors['success']}🏆 Excellent performance! You're a very strong runner.{self.colors['reset']}")
        elif pace <= 5:  # 5:00 min/km
            print(f"  {self.colors['info']}👍 Good performance! You're above average.{self.colors['reset']}")
        elif pace <= 6:  # 6:00 min/km
            print(f"  {self.colors['warning']}📈 Solid performance! Focus on consistency and gradual improvement.{self.colors['reset']}")
        else:
            print(f"  {self.colors['info']}🌱 Building foundation! Every run makes you stronger.{self.colors['reset']}")
        
        # Marathon prediction
        if metrics.distance_km < 42.195:
            marathon_time = 42.195 * metrics.pace_min_per_km
            marathon_str = self.minutes_to_time_str(marathon_time, True)
            print(f"  {self.colors['highlight']}🏃‍♂️ At this pace, you'd complete a marathon in: {marathon_str}{self.colors['reset']}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Pace Calculator - Calculate pace, time, and distance with beautiful output",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 10km in 45:00          # Calculate pace for 10km in 45 minutes
  %(prog)s marathon at 4:30        # Calculate time for marathon at 4:30 min/km pace
  %(prog)s 1:30:00 at 5:00        # Calculate distance for 1:30:00 at 5:00 min/km pace
  
Distance formats: 5km, 10k, 21.0975km, marathon, half-marathon, 1mi
Time formats: 45:00, 1:30:00, 1h30m, 90m
Pace formats: 4:30, 5.5 (minutes per kilometer)
        """
    )
    
    parser.add_argument("first_value", help="First value (distance, time, or pace)")
    parser.add_argument("preposition", choices=["in", "at"], help="Preposition: 'in' for time, 'at' for pace")
    parser.add_argument("second_value", help="Second value (distance, time, or pace)")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    
    args = parser.parse_args()
    
    try:
        # Create calculator instance first
        calculator = PaceCalculator()
        
        # Disable colors if requested
        if args.no_color:
            for key in calculator.colors:
                calculator.colors[key] = ""
        
        # Display banner
        calculator.print_banner()
        
        # Parse inputs
        if args.preposition == "in":
            # Format: distance in time
            distance, time = args.first_value, args.second_value
            pace = None
        else:  # args.preposition == "at"
            # Format: distance at pace OR time at pace
            # Check if first value is likely a time
            if calculator._is_likely_time(args.first_value):
                time, pace = args.first_value, args.second_value
                distance = None
            else:
                # First value is distance, second is pace
                distance, pace = args.first_value, args.second_value
                time = None
        
        # Calculate metrics
        metrics = calculator.calculate_metrics(distance, time, pace)
        
        # Display results
        calculator.display_results(metrics, distance, time, pace)
        
    except InputError as e:
        print(f"{calculator.colors['error']}❌ Input Error: {e}{calculator.colors['reset']}")
        sys.exit(1)
    except Exception as e:
        print(f"{calculator.colors['error']}❌ Unexpected error: {e}{calculator.colors['reset']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
