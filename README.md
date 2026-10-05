# GPS Positioning Simulator

A Python simulation that estimates a target's 2D position from its distances to three known reference points and studies how measurement noise affects positioning accuracy.

## Project Overview

The program begins with three known station locations and an unknown target location.

Using the measured distance from the target to each station, the system estimates the target's position.

The project then adds random measurement noise to simulate imperfect real-world distance measurements and compares the estimated position with the true position.

## Features

- Represents stations and targets as 2D points
- Calculates Euclidean distance between points
- Generates simulated distance measurements
- Estimates a target position from three reference stations
- Converts the geometry into a 2x2 linear system
- Solves the system using Cramer's Rule
- Adds random measurement noise
- Measures positioning error
- Runs repeated simulations
- Calculates average positioning error
- Visualizes stations, measured distances, true position, and estimated position

## Main File

- `gps.py` — contains the positioning model, simulation, error analysis, and visualization

## Core Mathematics

For a target at an unknown location `(x, y)` and a known station `(xi, yi)`, the distance relationship is:

**(x - xi)^2 + (y - yi)^2 = di^2**

Using three stations gives three circle equations.

The program subtracts the first circle equation from the other two. This removes the squared `x^2` and `y^2` terms and produces a 2x2 linear system.

That system is then solved using **Cramer's Rule** to estimate the target coordinates.

## Measurement Noise

Real measurements are rarely perfect.

To model this, the program adds a random value between `-noise` and `+noise` to each distance measurement.

It then estimates the position using the noisy distances and calculates:

**Position Error = Distance between true position and estimated position**

The simulation can repeat this process many times and calculate the average positioning error.

## Example

Suppose the three reference stations are:

- `(0, 0)`
- `(10, 0)`
- `(0, 10)`

and the true target position is:

- `(3, 4)`

The exact distances from the target to the three stations are calculated first.

With no measurement noise, the estimated location should be very close to:

**(3, 4)**

When noise is introduced, the estimated position moves slightly away from the true location, allowing the program to study how measurement uncertainty affects accuracy.

## Technologies and Concepts

- Python
- Linear algebra
- Geometry
- Euclidean distance
- Systems of linear equations
- Cramer's Rule
- Random simulation
- Error analysis
- Matplotlib

## Status

**Completed**

This project demonstrates how geometry, linear algebra, simulation, and numerical error analysis can be combined to model a simplified positioning system.
