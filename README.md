# 🏃‍♂️ Pace Calculator

A beautiful, feature-rich pace calculator for runners with colored output, training insights, and comprehensive metrics.

## ✨ Features

- **🎨 Beautiful Colored Output** - Cross-platform colored terminal output
- **📊 Comprehensive Metrics** - Distance, time, pace, and speed calculations
- **⏱️ Split Times** - Automatic calculation of splits for common distances
- **🔮 Projected Times** - See how your pace translates to other distances
- **🏃‍♂️ Training Zones** - Get training zone recommendations based on your pace
- **💡 Performance Insights** - Understand your performance level and get motivation

## 🚀 Installation

### Local Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Global Installation
Install globally to use from anywhere on your system:

```bash
# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x pacecalc.py

# Move to a directory in your PATH (e.g., /usr/local/bin on macOS/Linux)
sudo mv pacecalc.py /usr/local/bin/pacecalc

# Now you can run it from anywhere:
pacecalc 10km in 45:00
```

**Alternative (using pip):**
```bash
# Install dependencies first
pip install -r requirements.txt

# Install globally with pip
pip install -e .

# Or if you have a setup.py, you can use:
# pip install --user .
```

## 📖 Usage

### Basic Syntax
```bash
# If installed locally:
python pacecalc.py <first_value> <preposition> <second_value>

# If installed globally:
pacecalc <first_value> <preposition> <second_value>
```

### Examples

#### Calculate Pace (Distance + Time)
```bash
# 10km in 45 minutes
python pacecalc.py 10km in 45:00

# Marathon in 3:30:00
python pacecalc.py marathon in 3:30:00
```

#### Calculate Time (Distance + Pace)
```bash
# Marathon at 5:00 min/km pace
python pacecalc.py marathon at 5:00

# 10k at 4:30 min/km pace
python pacecalc.py 10k at 4:30
```

#### Calculate Distance (Time + Pace)
```bash
# 1 hour at 5:00 min/km pace
python pacecalc.py 1:00:00 at 5:00
```

### Input Formats

- **Distances**: `5km`, `10k`, `marathon`, `half-marathon`, `5mi`
- **Times**: `45:00`, `1:30:00`, `1h30m`, `90m`
- **Paces**: `4:30` (4:30 min/km), `5.5` (5.5 min/km)

## 🔧 Options

- `--no-color`: Disable colored output for compatibility

## 📚 Based On

This project is based on the original [pace-calculator](https://github.com/Wartijn/pace-calculator) by [Wartijn](https://github.com/Wartijn).
