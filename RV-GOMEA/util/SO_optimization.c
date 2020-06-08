/**
 *
 * RV-GOMEA
 *
 * If you use this software for any purpose, please cite the most recent publication:
 * A. Bouter, C. Witteveen, T. Alderliesten, P.A.N. Bosman. 2017.
 * Exploiting Linkage Information in Real-Valued Optimization with the Real-Valued
 * Gene-pool Optimal Mixing Evolutionary Algorithm. In Proceedings of the Genetic 
 * and Evolutionary Computation Conference (GECCO 2017).
 * DOI: 10.1145/3071178.3071272
 *
 * Copyright (c) 1998-2017 Peter A.N. Bosman
 *
 * The software in this file is the proprietary information of
 * Peter A.N. Bosman.
 *
 * IN NO EVENT WILL THE AUTHOR OF THIS SOFTWARE BE LIABLE TO YOU FOR ANY
 * DAMAGES, INCLUDING BUT NOT LIMITED TO LOST PROFITS, LOST SAVINGS, OR OTHER
 * INCIDENTIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR THE INABILITY
 * TO USE SUCH PROGRAM, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY
 * OF SUCH DAMAGES, OR FOR ANY CLAIM BY ANY OTHER PARTY. THE AUTHOR MAKES NO
 * REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF THE SOFTWARE, EITHER
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT. THE
 * AUTHOR SHALL NOT BE LIABLE FOR ANY DAMAGES SUFFERED BY ANYONE AS A RESULT OF
 * USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
 *
 * The software in this file is the result of (ongoing) scientific research.
 * The following people have been actively involved in this research over
 * the years:
 * - Peter A.N. Bosman
 * - Dirk Thierens
 * - Jörn Grahl
 * - Anton Bouter
 * 
 */

/*-=-=-=-=-=-=-=-=-=-=-=-=-=-= Section Includes -=-=-=-=-=-=-=-=-=-=-=-=-=-=*/
#include "SO_optimization.h"
/*-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=*/

/**
 * Returns 1 if x is better than y, 0 otherwise.
 * x is not better than y unless:
 * - x and y are both infeasible and x has a smaller sum of constraint violations, or
 * - x is feasible and y is not, or
 * - x and y are both feasible and x has a smaller objective value than y
 */



short betterFitness( double objective_value_x, double constraint_value_x, double objective_value_y, double constraint_value_y )
{
    short result;

    result = 0;

    if( constraint_value_x > 0 ) /* x is infeasible */
    {
        if( constraint_value_y > 0 ) /* Both are infeasible */
        {
            if( constraint_value_x < constraint_value_y ){
                   result = 1;}
        }
    }
    else /* x is feasible */
    {
        if( constraint_value_y > 0 ){ /* x is feasible and y is not */
           
            result = 1;}
        else /* Both are feasible */
        {
            if( objective_value_x < objective_value_y ){
            	result = 1;}
          
        }
    }

    return( result );
}


/*-=-=-=-=-=-=-=-=-=-=-=-=-=-= Section Problems -=-=-=-=-=-=-=-=-=-=-=-=-=-=*/
/**
 * Returns the name of an installed problem.
 */
char *installedProblemName( int index )
{
    switch( index )
    {
    case 14: return( (char *) "Circles in a Square" );
    }

    return( NULL );
}

/**
 * Returns the number of problems installed.
 */
int numberOfInstalledProblems( void )
{
    static int result = -1;

    if( result == -1 )
    {
        result = 0;
        while( installedProblemName( result ) != NULL )
            result++;
    }

    return( result );
}

/**
 * Writes the names of all installed problems to the standard output.
 */
void printAllInstalledProblems( void )
{
    int i, n;

    n = numberOfInstalledProblems();
    printf("Installed optimization problems:\n");
    for( i = 0; i < n; i++ )
        printf("%3d: %s\n", i, installedProblemName( i ));

    exit( 0 );
}

/**
 * Returns the lower-range bound of an installed problem.
 */
double installedProblemLowerRangeBound( int index, int dimension )
{
    switch( index )
    {

    case 14: return( ciasBRFunctionLowerRangeBound( dimension ) );

    }

    return( 0.0 );
}

/**
 * Returns the upper-range bound of an installed problem.
 */
double installedProblemUpperRangeBound( int index, int dimension )
{
    switch( index )
    {

    case 14: return( ciasBRFunctionUpperRangeBound( dimension ) );
   
    }

    return( 0.0 );
}

/**
 * Returns whether a parameter is inside the range bound of
 * every problem.
 */
short isParameterInRangeBounds( double parameter, int dimension )
{
    if( parameter < installedProblemLowerRangeBound( problem_index, dimension ) ||
            parameter > installedProblemUpperRangeBound( problem_index, dimension ) ||
            isnan( parameter ) )
    {
        return( 0 );
    }

    return( 1 );
}

/**
 * Initializes the parameter range bounds.
 */
void initializeParameterRangeBounds( void )
{
    int i;

    lower_range_bounds = (double *) Malloc( number_of_parameters*sizeof( double ) );
    upper_range_bounds = (double *) Malloc( number_of_parameters*sizeof( double ) );
    lower_init_ranges  = (double *) Malloc( number_of_parameters*sizeof( double ) );
    upper_init_ranges  = (double *) Malloc( number_of_parameters*sizeof( double ) );

    for( i = 0; i < number_of_parameters; i++ )
    {
        lower_range_bounds[i] = installedProblemLowerRangeBound( problem_index, i );
        upper_range_bounds[i] = installedProblemUpperRangeBound( problem_index, i );
    }

    for( i = 0; i < number_of_parameters; i++ )
    {
        lower_init_ranges[i] = lower_user_range;
        if( lower_user_range < lower_range_bounds[i] )
            lower_init_ranges[i] = lower_range_bounds[i];
        if( lower_user_range > upper_range_bounds[i] )
            lower_init_ranges[i] = lower_range_bounds[i];

        upper_init_ranges[i] = upper_user_range;
        if( upper_user_range > upper_range_bounds[i] )
            upper_init_ranges[i] = upper_range_bounds[i];
        if( upper_user_range < lower_range_bounds[i] )
            upper_init_ranges[i] = upper_range_bounds[i];
    }
}

/**
 * Returns the value of the single objective
 * and the sum of all constraint violations
 * function after rotating the parameter vector.
 * Both are returned using pointer variables.
 * Number of evaluations is increased by the
 * ratio ([0..1]) of new parameters that have
 * been changed.
 */
void installedProblemEvaluation( int index, double *parameters, double *objective_value, double *constraint_value, int number_of_touched_parameters, int *touched_parameters_indices, double *parameters_before, double objective_value_before, double constraint_value_before )
{
    double *rotated_parameters, *rotated_parameters_before, *touched_parameters, *touched_parameters_before, last_obj, last_cons;
    int i, j, c, prev_block, cur_block, *block_indices;

    touched_parameters = NULL;
    rotated_parameters = NULL;
    if( !(touched_parameters_indices == NULL || black_box_evaluations) )
    {
        touched_parameters = (double*) Malloc( number_of_touched_parameters*sizeof( double ) );
        for( i = 0; i < number_of_touched_parameters; i++ )
            touched_parameters[i] = parameters[touched_parameters_indices[i]];
    }

    if( rotation_angle == 0.0 )
    {
    
        if( touched_parameters_indices == NULL || black_box_evaluations ){
         installedProblemEvaluationWithoutRotation( index, parameters, objective_value, constraint_value, number_of_parameters, NULL, NULL, NULL, 0, 0 );}
         
        else {
        installedProblemEvaluationWithoutRotation( index, parameters, objective_value, constraint_value, number_of_touched_parameters, touched_parameters_indices, touched_parameters, parameters_before, objective_value_before, constraint_value_before );}
    }


    if( use_vtr && !vtr_hit_status && *constraint_value == 0 && *objective_value <= vtr  )
    {
        if( touched_parameters_indices != NULL )
            installedProblemEvaluation( index, parameters, objective_value, constraint_value, number_of_parameters, NULL, NULL, 0, 0 );
        if( *constraint_value == 0 && *objective_value <= vtr  )
        {
            
            vtr_hit_status = 1;
            elitist_objective_value = *objective_value;
            elitist_constraint_value = *constraint_value;
        }
    }

    if( !vtr_hit_status && betterFitness(*objective_value, *constraint_value, elitist_objective_value, elitist_constraint_value) )
    {
        
        elitist_objective_value = *objective_value;
        elitist_constraint_value = *constraint_value;
    }

    if( touched_parameters_indices != NULL )
        free( touched_parameters );
}

/**
 * Returns the value of the single objective
 * and the sum of all constraint violations
 * without rotating the parameter vector.
 * Both are returned using pointer variables.
 */
void installedProblemEvaluationWithoutRotation( int index, double *parameters, double *objective_value, double *constraint_value, int number_of_touched_parameters, int *touched_parameters_indices, double *touched_parameters, double *parameters_before, double objective_value_before, double constraint_value_before )
{
    *objective_value  = 0.0;
    *constraint_value = 0.0;
    if( black_box_evaluations || touched_parameters_indices == NULL )
    {
        switch( index )
        {
        
        case 14: ciasBRFunctionProblemEvaluation( parameters, objective_value, constraint_value ); break;
        
        }
        number_of_evaluations++;
    }
    else
    {
        switch( index )
        {
        
        case 14: ciasBRFunctionProblemEvaluation( parameters, objective_value, constraint_value ); break;

        }
        number_of_evaluations += number_of_touched_parameters/(double)number_of_parameters;
    }
}


void ciasBRFunctionProblemEvaluation( double *parameters, double *objective_value, double *constraint_value )
{

    int    i,k, j, nc;
    double result, xi0,xz1,xz0, xi1, xj0, xj1, distance;
    
    nc = number_of_parameters/2;
    
    for( i = 0; i < number_of_parameters; i++ )
    {
        if( parameters[i] < 0 )
            parameters[i] = 0;

        if( parameters[i] > 1 )
            parameters[i] = 1;
    }

    result = -1.0;
    int count = 2;
    int same =0;
    for( i = 0; i < nc; i++ ){
    	count=2;
        for( j = i+1; j < nc; j++ )
        {
            xi0      = parameters[2*i];
            xi1      = parameters[2*i+1];
            xj0      = parameters[2*j];
            xj1      = parameters[2*j+1];
            distance = (xi0-xj0)*(xi0-xj0) + (xi1-xj1)*(xi1-xj1);
           
	    if( result < 0 || distance < result ){
		    	 
		    	xarr[2*i] = xi0;
		    	xarr[2*i+1] = xi1;
		    	xarr[2*i+count] = xj0;
		    	xarr[2*i+count+1] = xj1;
		        result = distance;
	 
		    }
	
            
            
            
        }
     }  
            
            

                
        
     
     
    

    //fclose( file );
    result = sqrt( result );
    Darr[0]= result;
    *objective_value  = -result;
    *constraint_value = 0;
}

double ciasBRFunctionLowerRangeBound( int dimension )
{
    return( -1e+308 );
}

double ciasBRFunctionUpperRangeBound( int dimension )
{
    return( 1e+308 );
}

