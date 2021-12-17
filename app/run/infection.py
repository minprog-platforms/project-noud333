# Infection.py
# Noud Hover 12224693
# This script will simulate a virus using some parameters.
# These parameters run from the amount of particles to the size of the box.
# The time it takes for the virus to be cured and if it can be regained can also be chosen.
# Finally we have some ways people can selfisolate worked in.
# At the botom you will find the different simulations run and what I concluded from it.


import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import argparse
import json



# This function returns -1 50% of the time and 1 the other half.
# It is used to make random numbers range from -n to n instead of 0 to n.
def sign():
    sign_value = 1
    step = random.random()

    if step >= 0.5:
        sign_value = -1

    return sign_value



# This function returns particles back into the box.
# It checks if it is outside of the box. If so it will move the amount it has moved outside the box back into the box.
def boxcheck(position_check,box):
    position = position_check

    if position_check > box:
            position = box - abs((position_check-box))
    if position_check < -box:
        position = -box + abs((position_check +box))

    return position





# This function will generate a random step in x and y direction between +- stepsize.
# If fixed = 1 stepsize will be the radius of the step.
def random_step(stepsize,fixed):
    x_step = stepsize * random.random() * sign()

    if fixed == 1:
        y_step = sign() * (stepsize**2 - x_step**2)**(1/2)
    
    else:
        y_step = stepsize * random.random() * sign()

    return x_step, y_step






# This function will generate a list of random positions in a box for n_particles amount of particles.
# Box gives the size of the box. if box is 10, the box will go from -10 -> 10 in x and y direction.
# It will also create other starting conditions. Such as the status of particles (normal, infected, cured)
def startpos(n_particles,infected, box, isolation):
    x_pos = []
    y_pos = []
    infected_check = []
    isolating = []
    cure_status = []

    # Creating positions with random locations for the particles.
    for n in range(n_particles):
        positions = random_step(box,0)
        x_pos.append(positions[0])
        y_pos.append(positions[1])

    # Creating the status lists for the particles
    for n in range(n_particles):
        infected_check.append(0)
        isolating.append(0)
        cure_status.append(0)

    # Putting in the initial status of particles (by changing their value to 1)
    for n in range(infected):
        infected_check.pop(n)
        infected_check.insert(n,1)

    for n in range(isolation):
        isolating.pop(n)
        isolating.insert(n,1)
    
        
    # reverse the isolating list to make sure the first infected moves.
    # Infected will however stay still if that is an initial condition.
    isolating.reverse()



    return x_pos,y_pos, infected_check, isolating, cure_status






# This function moves every point in the list a random fixed amount.
def movement(stepsize,x_pos_list, y_pos_list,box, isolating, selfisolating_sick, symptom, cure_status):
    x_pos_step = []
    y_pos_step = []
    
    for n in range(len(x_pos_list)):

        # Checks if the point is selfisolating.
        if isolating[n] == 0:
            step = random_step(stepsize,1)
            x_step = x_pos_list[n]+ step[0]
            y_step = y_pos_list[n]+ step[1]
 
            # Returning the particle to the box
            x_step = boxcheck(x_step,box)
            y_step = boxcheck(y_step,box)

            # This part stops a particle if it notices its sick. symptom is the time to realise its sick.
            if selfisolating_sick ==1 and cure_status[n] >= symptom:
                isolating.pop(n)
                isolating.insert(n, 1)
        
        # In case the particle is selfisolating its position wont be changed.
        if isolating[n] == 1:
            x_step = x_pos_list[n]
            y_step = y_pos_list[n]
            

        x_pos_step.append(x_step)
        y_pos_step.append(y_step) 

    return  x_pos_step, y_pos_step





# This function checks if new particles are infected.
def infection_check(positions,infection_status, cure_status, cure_time, reinfect):
    cure_status_new = cure_status

    # For every infected particle the distance to other particles will be checked to see if they will be infected.
    for n in range(len(infection_status)):
        if infection_status[n] == 1:
            
            infection_status_new = []
            for m in range(len(infection_status)):

                # In case the infected particle is close enough to another uninfected particle it will change their
                # status to infected. 
                if infection_status[m] == 0:
                    distance = ((positions[0][n]-positions[0][m])**2+(positions[1][n]-positions[1][m])**2)**(1/2)
                    if distance <= 1:
                        infection_status_new.append(1)
                    else:
                        infection_status_new.append(0)
                # For the other cases the original status will be kept.
                if infection_status[m] == 1:
                    infection_status_new.append(1)
                
                if infection_status[m] ==2:
                    infection_status_new.append(2)
            infection_status = infection_status_new
        
            time = cure_status_new.pop(n)
            cure_status_new.insert(n,time+1)

            # This part of the code "cures" the particles.
            if time >=  cure_time and reinfect ==0:
                infection_status_new.pop(n)
                infection_status_new.insert(n,2)

            # If they can be reinfected people will be returned to normal instead of cured.
            if time >= cure_time and reinfect ==1:
                infection_status_new.pop(n)
                infection_status_new.insert(n,0)
                cure_status_new.pop(n)
                cure_status_new.insert(n,0)


    # This part creates the different frames.
    # It separates the points in 3 types so they can be plotted in different colors.
    frame_infected_x = []
    frame_infected_y = []

    frame_normal_x = []
    frame_normal_y = []

    frame_cured_x = []
    frame_cured_y = []

    for n in range(len(infection_status)):
        if infection_status[n] == 1:
            frame_infected_x.append(positions[0][n])
            frame_infected_y.append(positions[1][n])
        if infection_status[n] == 0:
            frame_normal_x.append(positions[0][n])
            frame_normal_y.append(positions[1][n])
        if infection_status[n] == 2:
            frame_cured_x.append(positions[0][n])
            frame_cured_y.append(positions[1][n])
    
    frame_infected = [frame_infected_x, frame_infected_y]
    frame_normal = [frame_normal_x, frame_normal_y]
    frame_cured = [frame_cured_x, frame_cured_y]
    
    frame = [frame_infected, frame_normal, frame_cured]
    return  infection_status, frame, cure_status_new



# This function is used in animation to create the next frame.
def ani_frame(frame_counter, simulation_list):

    for n in range(len(simulation_list)):
        plot_format(simulation_list[n],  frame_counter)

    return

# This function creates 2 plots per simulation you run simultatiously.
# N is the row in which the specific simulation is animated.
def plot_format(frames, frame_counter):
    boxsize = frames[4]
    x_points_inf = frames[0][frame_counter][0][0]
    y_points_inf = frames[0][frame_counter][0][1]
    
    x_points_norm = frames[0][frame_counter][1][0]
    y_points_norm = frames[0][frame_counter][1][1]

    x_points_cured = frames[0][frame_counter][2][0]
    y_points_cured = frames[0][frame_counter][2][1]


    axs[0].clear()
    axs[0].set(xlabel="X pos", ylabel="Y pos")
    axs[0].set_title("Infected particles: {}".format(len(x_points_inf)))
    axs[0].scatter(x_points_inf,y_points_inf, c="r")
    axs[0].scatter(x_points_norm,y_points_norm)
    axs[0].scatter(x_points_cured,y_points_cured, c="g")
    axs[0].set_xlim([-boxsize,boxsize])
    axs[0].set_ylim([-boxsize,boxsize])
    
    frames[1].append(len(frames[0][frame_counter][1][0]))
    frames[2].append(len(frames[0][frame_counter][0][0]))
    frames[3].append(len(frames[0][frame_counter][2][0]))
    axs[1].clear()
    axs[1].set(xlabel="Time", ylabel="Count")
    axs[1].plot(frames[1], c="b", label="Normal")
    axs[1].plot(frames[2], c="r", label="Infected")
    axs[1].plot(frames[3], c="g", label="Cured")
    axs[1].set_xlim([0,frames[5]])
    axs[1].legend()


# This function simulates the entire proces. It will return the frames to animate.
# It mostly runs other functions.
def simulation(cure_time, reinfect_check, selfisolating_sick, symptom,  amount_particles,amount_infected,boxsize,selfisolation, timesteps):
    init_cond = startpos(amount_particles,amount_infected,boxsize,selfisolation)
    infections = init_cond[2]
    isolating = init_cond[3]
    cure_status = init_cond[4]
    positions = [[init_cond[0],init_cond[1]]]
    frames = []

    # Here we calculate every step in the simulation.
    for n in range(timesteps):
        next_positions = movement(1, positions[-1][0],positions[-1][1],boxsize, isolating, selfisolating_sick, symptom, cure_status)

        next_infections = infection_check(next_positions,infections, cure_status, cure_time, reinfect_check)
        infections = next_infections[0]
        cure_status = next_infections[2]
        frames.append(next_infections[1])

    # These lists will be used to plot statistics in the animation.
    n_normal = []
    n_infected = []
    n_cured = []


    return frames, n_normal, n_infected, n_cured, boxsize, timesteps



def main(input, output):
    # These are the initial conditions for the simulation.
    # They will be saved in a usable way in init_cond via the startpos function.
    # These initial conditions would be litterally copied into init_cond. So they are added later.
    # Reinfect checks if people can get sick again after getting better.
    # selfisolation_after_sick stops movement of infected particles after symptom_time turns.
    # Symptom_time is the time to show symptoms. Must be larger than or equal to 1.

    file = open(input)
    data = json.load(file)

    amount_particles = data["amount_particles"]
    amount_infected = data["amount_infected"]
    boxsize = data["boxsize"]
    selfisolation = data["selfisolation"]
    timesteps = data["timesteps"]
    cure_time = data["cure_time"]
    reinfect = data["reinfect"]
    selfisolation_after_sick = data["selfisolation_after_sick"]
    symptom_time = data["symptom_time"]


    # Running the entire simulation
    simulation1 = simulation(cure_time, reinfect,selfisolation_after_sick, symptom_time, amount_particles,amount_infected,boxsize,selfisolation, timesteps)


    simulations = [simulation1]

    # Creating the animation and showing it.
    # It works with 2 simulations or more at the same time.
    global fig, axs
    fig, (axs) = plt.subplots(2)



    animation = FuncAnimation(fig, func=ani_frame, frames= np.arange(0,len(simulations[0][0])),interval=100, fargs=(simulations,))

    writergif = PillowWriter(fps=30)
    print(output)
    animation.save(output + '.gif',writer=writergif)



# The code currently looks at 3 different situations. On which 2 values are changed.
# On the top plot the people will continue their normal lives but are immume after recovering.
# The second plot has people continue with their normal lives. But they can catch the virus multiple times.

# What is interesting about this case is that when the people can catch it multiple times the curve will continue to increase.
# This is different from the case in which people recover for good. Where the virus "dies out" if its left alone in a corner.

# In the third case the virus can also be contracted multiple times. But the people will stay in place and "selfisolate"
# when they are aware that they are sick. In this case the total amount of infected people will be way lower. This may however
# be caused by the fact that they stay in isolation until the end of the simulation and essentially trap the virus in its place.
'''
# Initial conditions in the above described simulation
# The conditions seperated with / are the values changed between the 3 models.
amount_particles = 100
amount_infected = 1
boxsize = 10
selfisolation = 0
timesteps = 100
cure_time = 10
reinfect = 0 / 1 / 1
selfisolation_after_sick = 0 / 0 / 1
symptom_time = 2
'''

# Another set of simulations:
# In this simulation we varied the amount of people who selfisolate from the start of the simulation.
# In the first simulation the first 2 cases (0 an 20% selfisolating.) seemed to show little difference in total amount of people who
# caught the virus. With the 40% isolating case having about 20 less people who are sick.

# In later simulations the amount of people who are selfisolating seems to have an effect on the total amount of sick people
# from the start. With more people self isolating meaning that there are fewer people who become sick in total. It should be 
# noted however that the amount also seems strongly coralated with the starting positions of the virus and other particles.
# As this has a great effect on the final value.

'''
# Initial conditions in the above described simulation
# The conditions seperated with / are the values changed between the 3 models.
amount_particles = 100
amount_infected = 3
boxsize = 10
selfisolation = 0 / 20 / 40
timesteps = 100
cure_time = 10
reinfect = 0
selfisolation_after_sick = 0
symptom_time = 2
'''


# In this set we vary the size of the box. Which results in an larger average distance between particles.
# The amount of infected people corrolates highly with the density of people.
# In the case where the people are all very close to each other almost everyone will get the virus at a high speed.
# If the people are twice as far apart then the curve will flatten and the total amount of infected people also shrinks from
# everyone to most people. In the final case where they are 3x as far apart as the first situation
# the virus can't really spread and will thus die out quite fast.

'''
# Initial conditions in the above described simulation
# The conditions seperated with / are the values changed between the 3 models.
amount_particles = 100
amount_infected = 1
boxsize = 5 / 10 / 15
selfisolation = 0
timesteps = 100
cure_time = 10
reinfect = 0
selfisolation_after_sick = 0
symptom_time = 2
'''
# Final set of initial conditions:
# In this set we take the 2nd set. But let people stop moving once they know they are sick.
# In this case. The total amount of sick people is very low. It dies out quickly in any case.
# But the amount of selfisolating people definietly has an effect on the total amount of sick people.
# But this can differ between different initial conditions.
'''
# Initial conditions in the above described simulation
# The conditions seperated with / are the values changed between the 3 models.
amount_particles = 100
amount_infected = 1
boxsize = 10
selfisolation = 0 / 20 / 40
timesteps = 100
cure_time = 10
reinfect = 0
selfisolation_after_sick = 1
symptom_time = 2
'''
if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("input", help="python file of simulation")
    parser.add_argument("config", help="config file of simulation")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input, args.config)