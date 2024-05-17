#include "phylib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/// PART 1 ////
phylib_object * phylib_new_still_ball( unsigned char number,phylib_coord *pos ){

    phylib_object * pointer_still_ball =  malloc (sizeof(phylib_object)); // malloc space for a still ball
    pointer_still_ball->type = PHYLIB_STILL_BALL; // setting the enum for a still ball
    pointer_still_ball->obj.still_ball.number = number;  // setting the ball number 
    pointer_still_ball->obj.still_ball.pos.x = pos->x;  // setting the position x
    pointer_still_ball->obj.still_ball.pos.y = pos->y; // setting the position y

   return pointer_still_ball; // return the pointer 
}

phylib_object * phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ){

    phylib_object * pointer_rolling_ball =  malloc (sizeof(phylib_object)); // mallocing space for a rolling ball
    
    pointer_rolling_ball->type = PHYLIB_ROLLING_BALL; // setting the enum for a rolling ball

    pointer_rolling_ball->obj.rolling_ball.number = number; // setting the ball number

    pointer_rolling_ball->obj.rolling_ball.pos.x = pos->x; // setting the positon x
    pointer_rolling_ball->obj.rolling_ball.pos.y = pos->y; // setting the position y

    pointer_rolling_ball->obj.rolling_ball.vel.x = vel->x; // setting the velocity x
    pointer_rolling_ball->obj.rolling_ball.vel.y = vel->y; // setting the velocity y

    pointer_rolling_ball->obj.rolling_ball.acc.x = acc->x; // setting the acceleration
    pointer_rolling_ball->obj.rolling_ball.acc.y = acc->y; // setting the acceleration y

    return pointer_rolling_ball; // return the pointer
}

phylib_object *phylib_new_hole( phylib_coord *pos ){

    phylib_object * pointer_hole=  malloc (sizeof(phylib_object)); // mallocing space for a hole
    pointer_hole->type = PHYLIB_HOLE; // setting the enum for a hole

    pointer_hole->obj.hole.pos.x = pos->x; // setting the position x
    pointer_hole->obj.hole.pos.y = pos->y; // setting the position y

    return pointer_hole; // return the pointer
}

phylib_object *phylib_new_hcushion( double y ){

    phylib_object * pointer_hcushion=  malloc (sizeof(phylib_object)); // mallocing space for a horizontal cushion
    pointer_hcushion->type = PHYLIB_HCUSHION; // setthing the enum for a hcushion
    pointer_hcushion->obj.hcushion.y = y; // setting the y value of the hcushion

    return pointer_hcushion; // return the pointer
}


phylib_object *phylib_new_vcushion( double x ){

    phylib_object * pointer_vcushion=  malloc (sizeof(phylib_object)); // mallocing space for a vertical cushion
    pointer_vcushion->type = PHYLIB_VCUSHION; // setting the enum for a vcushion
    pointer_vcushion->obj.vcushion.x = x; //setting the x value for the vcushiom

    return pointer_vcushion; // return the pointer
}

phylib_table *phylib_new_table( void ){

    phylib_table * pointer_table = malloc (sizeof(phylib_table)); // mallocing space for the table
    pointer_table->time = 0.0;  // setting the time to 0.0

    for(int i = 0; i<PHYLIB_MAX_OBJECTS;i++){ // anloop over all objects of the table, following the assignment instructions, we call the above functions
         if(i == 0){                          // based on the index we call functions : new ball (rolling/still), new cushion (v & h cushion), and holes, the rest are null
            pointer_table->object[i]= phylib_new_hcushion(0.0); 
         }
        else if(i == 1){
            pointer_table->object[i]= phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
         }
        else if(i == 2){
            pointer_table->object[i]= phylib_new_vcushion(0.0);            
        }
        else if(i == 3){
            pointer_table->object[i]= phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
        }
       else if(i == 4){ // hole 1 
            phylib_coord pos;
            pos.x = 0.0;
            pos.y = 0.0;
            pointer_table->object[i]= phylib_new_hole(&pos);
        }
        else if(i == 5){ // hole 2 
            phylib_coord pos;
            pos.x = 0.0;
            pos.y = PHYLIB_TABLE_WIDTH;
            pointer_table->object[i]= phylib_new_hole(&pos);
        }
        else if(i == 6){ // hole 3
            phylib_coord pos;
            pos.x = 0.0;
            pos.y = PHYLIB_TABLE_LENGTH;
            pointer_table->object[i]= phylib_new_hole(&pos);
        }
       else if(i == 7){ // hole 4
            phylib_coord pos;
            pos.x = PHYLIB_TABLE_WIDTH;
            pos.y = 0.0;
            pointer_table->object[i]= phylib_new_hole(&pos);
        }
        else if(i == 8){ // hole 5 
            phylib_coord pos;
            pos.x = PHYLIB_TABLE_WIDTH;
            pos.y = PHYLIB_TABLE_WIDTH;
            pointer_table->object[i]= phylib_new_hole(&pos);
        }
        else if(i == 9){ // hole 6 
            phylib_coord pos;
            pos.x = PHYLIB_TABLE_WIDTH;
            pos.y = PHYLIB_TABLE_LENGTH;
            pointer_table->object[i]= phylib_new_hole(&pos); 
        }
        else{
            pointer_table->object[i] = NULL;
        }
    }
    
    return pointer_table; // return the pointer to the table with intilzed objects
}

//// PART 2 ////

void phylib_copy_object( phylib_object **dest, phylib_object **src ){

    if(* src == NULL){ // if src is pointing to null set the destination pointer to null
        * dest = NULL;
    }
    else{
        phylib_object * new_object =  malloc (sizeof(phylib_object)); // malloc space for the new object
        * dest = new_object; // set the destination to the new object 
        memcpy(*dest,*src,sizeof(phylib_object)); // use memcpy to copy the object for the src to the dest with the size of phylib_object
    } 
}

phylib_table *phylib_copy_table( phylib_table *table ){

    if (table == NULL){ // if the table is null return null
        return NULL;
    }
    else{
        phylib_table * new_table = malloc (sizeof(phylib_table)); // malloc space for the copy of the table
        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++){
            new_table->object[j] = NULL; // setting all the objects in the copy table to null so we have no unknown values in the copy
        }

        for(int i = 0;i<PHYLIB_MAX_OBJECTS; i++){
            phylib_copy_object(&new_table->object[i],&table->object[i]); // using the copy object function we go over all the objects in the table and copy it
        }
        new_table->time = table->time; // set the time of the new table with the old tables time
        return new_table; // return the copy of the orignal table
    }
}

void phylib_add_object( phylib_table *table, phylib_object *object ){
    
    for(int i = 0;i<PHYLIB_MAX_OBJECTS; i++){
        if (table->object[i] == NULL){ // if the object is null, indicating that there is no object there, assign it an object
            table->object[i] = object;
            return ;
        }
    }
}

void phylib_free_table( phylib_table *table ){
    
    if(table!= NULL){ // if the table is not empty free all the objects 
        for(int i = 0;i<PHYLIB_MAX_OBJECTS; i++){
            free(table->object[i]);
         }
    free(table); // then free the table structure 
    }
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){

   phylib_coord difference;
   difference.x = (c1.x-c2.x); // subtract the x coordinates of both objects
   difference.y = (c1.y-c2.y); // subtract the y coordintes of both objects 
   return difference; // return the difference
}

double squareIt(double x){ // helper function I made for squaring 

    return (x*x); // return the squared value
}

double phylib_length( phylib_coord c ){

    double length = squareIt(c.x) + squareIt(c.y); // using my helper square both the x and y values and add them
    double result = sqrt(length); // using the sqrt() to square the above line
    return result; // return the resulting length
}

double phylib_dot_product( phylib_coord a, phylib_coord b ){

    double dot_product = (a.x * b.x) + (a.y * b.y); // calculating the dot product 
    return dot_product; // return the dot product 
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){
    
    phylib_coord difference; // the following variables I need (since I cant intilize them within the switch statements)
    difference.x = 0.0;
    difference.y = 0.0;
    double length = 0.0;
    double distance = 0.0; 
    double absoluteDistance = 0.0;

    if(obj1->type != PHYLIB_ROLLING_BALL){ // object one is not a rolling ball return -1
        return -1.0;
    }
    else {
        switch(obj2->type){ // switch stament cases are based on the enum of object 2
        // the distance formula is ((x1 + x2)^2 + (y1 +y2)^2) and sqaure root the result 
        // this formula is replicated by using the combination of phylib_sub() and phylib_length()
        // and then sumbtracting it by the radius
        case 0 : // still ball
            difference = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
            length = phylib_length(difference);
            distance = length - PHYLIB_BALL_DIAMETER;
            return distance; 
            break;
        case 1: // rolling ball
            difference = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
            length = phylib_length(difference);
            distance = length - PHYLIB_BALL_DIAMETER;
            return distance; 
            break;
        case 2: // hole
            difference = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
            length = phylib_length(difference);
            distance = length - PHYLIB_HOLE_RADIUS;
            return distance;
            break;
        case 3: // hcushion - use absolute value since in 1 Dimension
            absoluteDistance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y); 
            distance = absoluteDistance - PHYLIB_BALL_RADIUS ;
            return distance;
            break;
        case 4: // vcushion - use absolute value since in 1 Dimension
            absoluteDistance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x); 
            distance = absoluteDistance - PHYLIB_BALL_RADIUS ;
            return distance;
            break;
        default: // if none of the options return -1
            return -1;

        }
    }
}

//// PART 3 ////

void phylib_roll( phylib_object *new, phylib_object *old, double time ){
    if(new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL){
        // do nothing if the first and second object are not rolling balls
        return ; // [CHANGED] this should exit now so it wont print if if anything entered is not a rolling ball
    }
    double half = 0.5;
    double squardTime = squareIt(time);
    new->obj.rolling_ball.pos.x = (old->obj.rolling_ball.pos.x) + ((old->obj.rolling_ball.vel.x)*(time)) + ((half)*(old->obj.rolling_ball.acc.x)*(squardTime)); 
    new->obj.rolling_ball.pos.y = (old->obj.rolling_ball.pos.y) + ((old->obj.rolling_ball.vel.y)*(time)) + ((half)*(old->obj.rolling_ball.acc.y)*(squardTime)); 

    new->obj.rolling_ball.vel.x = (old->obj.rolling_ball.vel.x) + ((old->obj.rolling_ball.acc.x)*(time)); 
    new->obj.rolling_ball.vel.y = (old->obj.rolling_ball.vel.y) + ((old->obj.rolling_ball.acc.y)*(time));

    if((new->obj.rolling_ball.vel.x) * (old->obj.rolling_ball.vel.x) < 0){ // multiplying the old and new velocity of both x &y
        new->obj.rolling_ball.vel.x = 0;                                   // if the value is less than 0 then we know that the signs changed 
        new->obj.rolling_ball.acc.x = 0;                                   // set the vel and acc to zero
    }  
    if((new->obj.rolling_ball.vel.y) * (old->obj.rolling_ball.vel.y) < 0){ 
        new->obj.rolling_ball.acc.y = 0;
        new->obj.rolling_ball.vel.y = 0;
    }
    
} 

unsigned char phylib_stopped( phylib_object *object ){
    double speed = phylib_length(object->obj.rolling_ball.vel); // we need the length of the velocity to get the speed
    unsigned char saved_number = object->obj.rolling_ball.number; // saving the number and the positions to transfer it after we change it to still
    double saved_posx = object->obj.rolling_ball.pos.x;
    double saved_posy = object->obj.rolling_ball.pos.y;

    if(speed < PHYLIB_VEL_EPSILON){ // if the the speed is less the the PHYLIB_VEL_EPSILON convert it to a still ball
        object->type = PHYLIB_STILL_BALL;
        object->obj.rolling_ball.number = saved_number;
        object->obj.rolling_ball.pos.x = saved_posx;
        object->obj.rolling_ball.pos.y = saved_posy; // [CHANGED] it was pos.x = saved_posy
        return 1; // return 1 indicate the conversion
    }

    return 0; // return 0 to indicate there was no conversion
}

    void phylib_bounce( phylib_object **a, phylib_object **b ){
        unsigned char saved_number = (*b)-> obj.rolling_ball.number; // saving the values of the ball number and position
        phylib_coord saved_pos = (*b)-> obj.rolling_ball.pos;
        phylib_coord r_ab; // creating variables given in the assignment instructions 
        r_ab.x = 0.0;
        r_ab.y = 0.0;
        phylib_coord v_rel;
        v_rel.x = 0.0;
        v_rel.y = 0.0;

        phylib_coord n;
        n.x = 0.0;
        n.y = 0.0;

        double v_rel_n = 0.0;
        double speed_a = 0.0;
        double speed_b = 0.0;

        
        switch((*b)->type){ // cases are based on the enum of object b
        case 3 : // hcushion
            (*a)->obj.rolling_ball.vel.y= (((*a)->obj.rolling_ball.vel.y)*(-1)); //[CHANGED] I put it as the position before, i meant velocity
            (*a)->obj.rolling_ball.acc.y = (((*a)->obj.rolling_ball.acc.y)*(-1));
            break;
        case 4 : // vchushion
            (*a)->obj.rolling_ball.vel.x= (((*a)->obj.rolling_ball.vel.x)*(-1)); // [CHANGED] I put it as the position before, i meant velocity
            (*a)->obj.rolling_ball.acc.x= (((*a)->obj.rolling_ball.acc.x)*(-1));
            break;
        case 2: // hole
           free(* a);
           (* a) = NULL;
           break;
        case 0 : // still ball - no break since we want it to become a rolling ball 
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.number = saved_number;

            (*b)-> obj.rolling_ball.pos = saved_pos;

            (*b)->obj.rolling_ball.vel.x = 0.0; // initializng the vel and acc because still ball doesnt have them, we need them for the next case (no break)
            (*b)->obj.rolling_ball.vel.y = 0.0;

            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;
            
        case 1 : // rollling
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos,(*b)->obj.rolling_ball.pos);
            v_rel = phylib_sub((*a)->obj.rolling_ball.vel,(*b)->obj.rolling_ball.vel);

            n.x = (r_ab.x)/(phylib_length(r_ab));
            n.y = (r_ab.y)/(phylib_length(r_ab));

            v_rel_n = phylib_dot_product(n,v_rel);

           (*a)->obj.rolling_ball.vel.x = ((*a)->obj.rolling_ball.vel.x) - (v_rel_n * n.x); 
           (*a)->obj.rolling_ball.vel.y = ((*a)->obj.rolling_ball.vel.y) - (v_rel_n * n.y);

           (*b)->obj.rolling_ball.vel.x = ((*b)->obj.rolling_ball.vel.x) + (v_rel_n * n.x); 
           (*b)->obj.rolling_ball.vel.y = ((*b)->obj.rolling_ball.vel.y) + (v_rel_n * n.y);

           speed_a = phylib_length((*a)->obj.rolling_ball.vel); 
           speed_b = phylib_length((*b)->obj.rolling_ball.vel);

           if(speed_a > PHYLIB_VEL_EPSILON){
            (*a)->obj.rolling_ball.acc.x = (((*a)->obj.rolling_ball.vel.x)*(-1)) / (speed_a)*PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc.y = (((*a)->obj.rolling_ball.vel.y)*(-1)) / (speed_a)*PHYLIB_DRAG;
           }
           if(speed_b > PHYLIB_VEL_EPSILON){
            (*b)->obj.rolling_ball.acc.x = (((*b)->obj.rolling_ball.vel.x)*(-1)) / (speed_b)*PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc.y = (((*b)->obj.rolling_ball.vel.y)*(-1)) / (speed_b)*PHYLIB_DRAG;
           }      
            break;
    }

}

unsigned char phylib_rolling( phylib_table *t ){
    unsigned char counter = 0; // counter for number of rolling balls
    
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL){ // conditions for a rolling ball
            counter++;
        }
    }
    return counter; // return the number of balls
}

phylib_table *phylib_segment( phylib_table *table ){
    double my_time = PHYLIB_SIM_RATE; // creating my own time varibles to increment and send to the copy
    unsigned char convert = 0; // the returned unsigned char from the roll function
    double distance = 0.0; // initilizing the distance to zero
    unsigned char number_rolling = 0; // number of rolling bals

    number_rolling = phylib_rolling(table); // check for the number of rolling balls

    if(number_rolling <= 0){ // if the number of rolling balls is less than or equal to zero return null
        return NULL;
    }
    
    phylib_table * copy = phylib_copy_table(table); // if number of rolling balls is > 0 hen copy the table

    while(my_time < PHYLIB_MAX_TIME){ // first condtion that will terminate the function is, if my_time is more that the max time 
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if(copy->object[i] != NULL && copy->object[i]->type == PHYLIB_ROLLING_BALL){
                phylib_roll(copy->object[i],table->object[i],my_time); // while the above conditons are true roll the balls
            }
        }
// distance - the following code block is used to calculate distance, using a nested for loop we compare one object on the copy to another
            for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
                if(copy->object[i] != NULL){
                    for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++){
                        if(copy->object[j] != NULL && copy->object[i]->type == PHYLIB_ROLLING_BALL && i != j ){
                            distance = phylib_distance(copy->object[i],copy->object[j]);
                            if(distance <= 0){ // the second condition for termination of function is if the distance is equal and less than zero
                                phylib_bounce(&copy->object[i],&copy->object[j]);  // apply the bounce function
                                copy->time += my_time; // increment the time by my time variable
                                return copy; // then return the copy of the function
                            }
                        }
                    }
                }
            }
// stopped - the follwing code block for a stopped ball
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if(copy->object[i] != NULL && copy->object[i]->type == PHYLIB_ROLLING_BALL){
                convert = phylib_stopped(copy->object[i]); // after the above condtion is true then check to see if the ball is stopped
                if (convert > 0){ // the third condtion is if the ball is a still ball terminate the program, this means if the convert variable is >0
                    copy->time += my_time; // if yes, increment the copy's time by my time variable 
                    return copy; // thern return the copy of the function
                }
            }
        }

       my_time += PHYLIB_SIM_RATE; // increment the time by the sim rate
    }
    copy->time += my_time; // update the copy's time by the my time variable 
    return copy; // return the copied table
}

// added function
char *phylib_object_string( phylib_object *object ){
    static char string[80];

    if (object==NULL){
    snprintf( string, 80, "NULL;" );
    return string;
    }
    
    switch (object->type){
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,"STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,"ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,"HOLE (%6.1lf,%6.1lf)",object->obj.hole.pos.x,object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,"HCUSHION (%6.1lf)",object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,"VCUSHION (%6.1lf)",object->obj.vcushion.x );
            break;
    }
    return string;
}
