#! /bin/bash
dir=$1
instance=$2 

cmd="/home/or/.jdks/openjdk-16/bin/java -javaagent:/home/or/Programs/idea-IU-211.6693.111/lib/idea_rt.jar=46745:/home/or/Programs/idea-IU-211.6693.111/bin -Dfile.encoding=UTF-8 -classpath rddlsim-master/out/production/rddlsim-master:rddlsim-master/lib/commons-math3-3.2.jar:rddlsim-master/lib/xercesImpl.jar:rddlsim-master/lib/grappa1_4.jar:rddlsim-master/lib/jlex.jar:rddlsim-master/lib/xml-apis.jar:rddlsim-master/lib/java_cup.jar rddl.sim.Simulator $dir $instance"


echo $($cmd)
