num_of_step=1000
code = """//////////////////////////////////////////////////////////////////////////////////////////
// swarm_of_locusts{num_of_step} Domain by Or Wertheim
//  _____________
//  3|@c1|@c2|@c3|
//  2|@c4|@c5|@c6|
//  1|@c7|@c8|@c9|
//  --------------
//y/x  1   2   3

domain swarm_of_locusts{num_of_step} {{
types {{
		cell : object;
		direction : {{@up, @down, @left,@right}};
	}};

pvariables {{ 
x_location(cell) : {{non-fluent, int, default = -1}};
y_location(cell) : {{non-fluent, int, default = -1}};

tons_of_plants(cell) : {{state-fluent, real, default = 10.0}}; 


swarm_disabled : {{state-fluent, bool, default = false}};
swarm_location_x : {{state-fluent, int, default = 1}};
swarm_location_y : {{state-fluent, int, default = 1}}; """.format(num_of_step=str(num_of_step))
counter=1
for i in range(num_of_step):
    step=i+1
    step1 = counter
    counter = counter + 1
    step2 = counter
    counter=counter+1
    step3 = counter
    counter=counter+1
    step4 = counter
    counter=counter+1
    code = code + """
total_neighbors_plants{stepC} : {{interm-fluent, real, level = {stepC1}}};
swarm_move{stepC} : {{interm-fluent, direction, level = {stepC2}}};
swarm_location{stepC}_x : {{ interm-fluent, real, level = {stepC3}}};
swarm_location{stepC}_y : {{ interm-fluent, real, level = {stepC3}}};""".format(stepC=str(step), stepC1=str(step1), stepC2=str(step2), stepC3=str(step3))
    if i < num_of_step-1:
        code = code + """
tons_of_plants{stepC}(cell) : {{ interm-fluent, real, level = {stepC4}}};""".format(stepC=str(step), stepC4=str(step4))

code = code + """
disable_swarm_act(cell) : { action-fluent, bool, default = 0};
};
cpfs{
"""
for i in range(num_of_step):
    step1=str(i+1)
    step0 = str(i)
    if i == 0:
        step0 = ''
    code = code + """
total_neighbors_plants{stepC1} = sum_{{?c : cell}}[if (((swarm_location{stepC0}_x+1) == x_location(?c) ^ swarm_location{stepC0}_y == y_location(?c)) |
((swarm_location{stepC0}_x - 1) == x_location(?c) ^ swarm_location{stepC0}_y == y_location(?c)) | 
((swarm_location{stepC0}_y + 1) == y_location(?c) ^ swarm_location{stepC0}_x == x_location(?c)) |
((swarm_location{stepC0}_y -1) == y_location(?c) ^ swarm_location{stepC0}_x == x_location(?c))) then tons_of_plants{stepC0}(?c) else 0.0];

swarm_move{stepC1} = Discrete(direction, 
						@up : if(swarm_location{stepC0}_y == 3) then 0.0 else (sum_{{?c : cell}}[if ((swarm_location{stepC0}_y + 1) == y_location(?c) ^ swarm_location{stepC0}_x == x_location(?c)) then tons_of_plants{stepC0}(?c) else 0.0])/total_neighbors_plants{stepC1},
						@down : if(swarm_location{stepC0}_y == 1) then 0.0 else (sum_{{?c : cell}}[if ((swarm_location{stepC0}_y - 1) == y_location(?c) ^ swarm_location{stepC0}_x == x_location(?c)) then tons_of_plants{stepC0}(?c) else 0.0]/total_neighbors_plants{stepC1}),
						@left : if(swarm_location{stepC0}_x == 1) then 0.0 else (sum_{{?c : cell}}[if ((swarm_location{stepC0}_x - 1) == x_location(?c) ^ swarm_location{stepC0}_y == y_location(?c)) then tons_of_plants{stepC0}(?c) else 0.0]/total_neighbors_plants{stepC1}),
						@right :if(swarm_location{stepC0}_x == 3) then 0.0 else (sum_{{?c : cell}}[if ((swarm_location{stepC0}_x + 1) == x_location(?c) ^ swarm_location{stepC0}_y == y_location(?c)) then tons_of_plants{stepC0}(?c) else 0.0]/total_neighbors_plants{stepC1})
					);

swarm_location{stepC1}_x = switch(swarm_move{stepC1})
{{
case @up: swarm_location{stepC0}_x,
case @down: swarm_location{stepC0}_x,
case @right: swarm_location{stepC0}_x + 1,
case @left: swarm_location{stepC0}_x - 1
}}; 

swarm_location{stepC1}_y = switch(swarm_move{stepC1})
{{
case @up: swarm_location{stepC0}_y + 1,
case @down: swarm_location{stepC0}_y - 1,
case @right: swarm_location{stepC0}_y,
case @left: swarm_location{stepC0}_y
}};""".format(stepC0=step0, stepC1=step1)
    if i < num_of_step-1:
        code=code+"""
tons_of_plants{stepC1}(?c)= if (swarm_location{stepC1}_y == y_location(?c) ^ swarm_location{stepC1}_x == x_location(?c)) then tons_of_plants{stepC0}(?c)*0.5 else tons_of_plants{stepC0}(?c);""".format(stepC0=step0, stepC1=step1)


code=code+"""
swarm_location_x'=swarm_location{steps1}_x;
swarm_location_y'=swarm_location{steps1}_y;
tons_of_plants'(?c)=if (swarm_disabled) then tons_of_plants(?c) else (if (swarm_location{steps1}_y == y_location(?c) ^ swarm_location{steps1}_x == x_location(?c)) then tons_of_plants{steps0}(?c)*0.5 else tons_of_plants{steps0}(?c));

swarm_disabled' = if (swarm_disabled) then swarm_disabled else exists_{{?c : cell}} ((disable_swarm_act(?c) == 1)^ x_location(?c) == swarm_location{steps1}_x ^ y_location(?c) == swarm_location{steps1}_y);
}};
""".format(steps1=str(num_of_step), steps0=str(num_of_step-1))

code = code+"""
	reward = [sum_{{?c : cell}}(tons_of_plants'(?c))];
	
}}

non-fluents swarm_of_locusts{num_of_step}_nf {{

	domain = swarm_of_locusts{num_of_step};
	objects {{
		cell : {{cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9}};
	}};
	non-fluents {{ 
x_location(cell1)=1;
x_location(cell2)=2;
x_location(cell3)=3;
x_location(cell4)=1;
x_location(cell5)=2;
x_location(cell6)=3;
x_location(cell7)=1;
x_location(cell8)=2;
x_location(cell9)=3;

y_location(cell1)=3;
y_location(cell2)=3;
y_location(cell3)=3;
y_location(cell4)=2;
y_location(cell5)=2;
y_location(cell6)=2;
y_location(cell7)=1;
y_location(cell8)=1;
y_location(cell9)=1;
 
}};
}}

instance inst_swarm_of_locusts{num_of_step} {{

	domain = swarm_of_locusts{num_of_step};
	
	non-fluents = swarm_of_locusts{num_of_step}_nf;
  
	init-state {{ 
swarm_location_x=2;
swarm_location_y=2;
	}};
  
	max-nondef-actions = 1;
  
	horizon  = 9;
	discount = 0.9;
}}


""".format(num_of_step=str(num_of_step))
# open text file
text_file = open("generate_swarm_domain.rddl", "w")

# write string to file
text_file.write(code)

# close file
text_file.close()