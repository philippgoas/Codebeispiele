/**
 * @file controller.cpp
 * @brief Implementation file for the PIDController class.
 *
 * This file contains the implementation of the PIDController class,
 * which implements a PID (Proportional-Integral-Derivative) controller
 * for controlling the inverted pendulum system.
 *
 * @author [Philipp Goas, Daniel Goldmann]
 */

#include "controller.h"
#include <iostream>

PIDController::PIDController() { update_params(kp, kd, ki); }

void PIDController::setClamp(double max, double min) {
  ///@todo Implement setClamp for setting the output limits
  max_output = max; //Initilize new parameters min_output and max_output to set limits for the simulation
  min_output = min;
}

double PIDController::output(double error) {
  ///@todo Implement the PID controller output calculation
  double dt = 0.0001;   //set dt equal to delta_t in simulator_h to calculate the derivate
  double derivate = (error - previous_error) / dt;  //Calculation of the derivate for the output of Kd
  integral += error * dt; //Calculation of the integral for the output of Ki

  double output = kp * error + kd * derivate + ki * integral; //Calculation of the output with variables Kp, Ki and Kd of a PID-Controller

  //Set the specified limits to the output
  if (output > max_output) {    //if the output is higher than max_output is initialized than the output is limited with max_output and will be reduced
      output = max_output;      //by the integral to prevent overshooting
      integral -= error * dt;   
  } else if (output < min_output) {    //if the output is lower than min_output is initialized than the output is limited with min_output and will be 
      output = min_output;             //reduced by the integral to prevent overshooting
      integral -= error * dt;
  }

  previous_error = error;   //update previous_error to work with new variables

  return output;
}

void PIDController::update_params(double kp_, double kd_, double ki_) {
  ///@todo Implement the update_params function for PID controller
  kp = kp_; 
  kd = ki_; //update kp, ki and kd to regulate with this parameters in next cycle
  ki = kd_;
}
void PIDController::reset() {
  ///@todo Implement the reset function for PID controller called by simulator
  /// when simulation is reset
  integral = 0.0;         //set integral to 0 return to the initial state
  previous_error = 0.0;   //set previous_error to 0 to return to initial state
}
