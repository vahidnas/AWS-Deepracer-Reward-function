import math

def reward_function(params):
    # Example of penalize steering, which helps mitigate zig-zag behaviors

    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    abs_steering = abs(params['steering_angle']) # Only need the absolute steering angle
    steps = params['steps']
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    is_offtrack = params['is_offtrack']
    is_reversed = params['is_reversed']
    
    SPEED_THRESHOLD = 2.0
    
    # Intialize reward with a typical value
    reward = 1.0
    

    # Penalize if the car is off the track
    if not is_offtrack:
        reward = 1.0
    else:
        reward = 1e-3


    # Penalize if the car is reversed
    if not is_reversed:
        reward = 1.0
    else:
        reward = 1e-3


    # Calculate the distance from each border
    distance_from_border = 0.5 * track_width - distance_from_center
    
    #Reward higher if the car stays inside the track borders
    if distance_from_border >= 0.05:
        reward = 1.0
    else:
        reward = 1e-3   #low reward if too close to the border of goes off track


    #calculate the direction of the center line based on the closest waypoint
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    
    # Calculate the diiference in radius, arctan2(dy,dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)
    

    # Calculate the diffrenece between the track direction and the heading direction of the car
    direction_diff = abs (track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
        

    # Penalize if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    vid = 1
    if direction_diff > DIRECTION_THRESHOLD:
        vid = 1 - (direction_diff / 50)
    if vid < 0 or vid > 1:
        vid = 0
        reward *= vid
    

    if not all_wheels_on_track:
        # Penalize if the car goes off the track
        reward = 1e-3
    elif speed < SPEED_THRESHOLD:
        # Penalize if the car goes too slow
        reward *= 0.5
    else:
        #High reward if car stays on track and goes fast
        reward += 1.0
    

    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward *= 0.5
    elif distance_from_center <= marker_3:
        reward *= 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 15 
    
    # Penalize reward if the car is steering too much
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8
        
    # Total number of steps we want a car to finish the lap
    TOTAL_NUM_STEPS = 300
    

    #Give additional reward if the pass every 100 steps faster than expected
    if(steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100:
        reward  += 10.0
    return float(reward)
