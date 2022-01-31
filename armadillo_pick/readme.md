
## AOS Gazebo simulation experiments
We experimented with our basic skills before documenting their (probabilistic) behavior using PLPs.</br>
Our skills are:
- **Pick** 
-  **Serve** (can to person) 
-  **Navigate** 
-  **Observe** (if holding can).

### Experiments
We constructed a gazebo world that contains a room with two tables. A can is placed on each table. one can is easy to pick while the other is very difficult (we scaled the collision on the z-axis to be 0.2, making it like a disk). A person is located on the corridor outside the room, and the robot should pick one of the cans and deliver it to the person. The experiment starts with the robot facing the table with the difficult-to-pick can. </br>
#### Experiment Scene
<img src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/experiment scene.png" data-canonical-src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/experiment scene.png" height="400"/>

#### Scenarios

<img src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/experiment_scenarios2.png" data-canonical-src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/experiment_scenarios2.png" height="400"/>
We performed "scenario 1" ten times and "scenario 2" eleven times, collected the statistics about the skill execution (what happened and what the skill reported), and calculated their probabilistic behavior model.

#### Skills statistics

<img src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/skills_statistics.png" data-canonical-src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/skills_statistics.png" />

#### Skills model
<img src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/Skills_model.png" data-canonical-src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/Skills_model.png" />

### Images of (some) Skill modes

#### Pick action modes:

Successful pick             |  Partially successful pick, dangerous to serve to a person             |  Failed to pick, can was dropped
:-------------------------:|:-------------------------:|:-------------------------:
<img src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/pick_success.png" data-canonical-src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/pick_success.png" width="300" height="300" />  |  <img src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/pick_finished_in_dangerous_state.png" data-canonical-src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/pick_finished_in_dangerous_state.png" width="300" height="300" />  |  <img src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/pick_failed_dropped_can.png" data-canonical-src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/pick_failed_dropped_can.png" width="300" height="300" />

 
#### Deliver can action modes:

Successful can delivery             |  person wounded during can delivery after a partially successful pick             
:-------------------------:|:-------------------------: 
<img src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/serve_person_success.png" data-canonical-src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/serve_person_success.png" width="300" height="300" />  |  <img src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/serve_person_failed_person_Wounded2.png" data-canonical-src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/serve_person_failed_person_Wounded2.png" width="300" height="300" /> <img src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/serve_person_failed_person_Wounded.png" data-canonical-src="https://github.com/orhaimwerthaim/AOS-experiments/blob/main/armadillo_pick/images/serve_person_failed_person_Wounded.png" width="300" height="300" /> 
