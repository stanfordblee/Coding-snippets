// A simulation of 3 heroes fighting a boss in an RPG
// Created on 01/08/2020
//
// User inputs a 'lucky number', and then simulation is executed
// Heroes and boss attack simultaneously - if hero is defeated, switch to next hero

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define TEAM_SIZE 3
#define MAX_LENGTH 100

// Creating struct for character, used for both adventurer and boss
struct character {
	char class[MAX_LENGTH];
	char ability[MAX_LENGTH];
	int power;
	int health;
};

int randomise(void);

int still_alive(struct character *boss, struct character hero[TEAM_SIZE]);

void attack(struct character *attacker, struct character *defender);

void end_fight(struct character *boss);

int main (void) {
	
	// Hero character array
	struct character hero[TEAM_SIZE];
	
	// For hero 1 of 3: Knight
	strcpy(hero[0].class, "Knight");
	strcpy(hero[0].ability, "Gigas Wave");
	hero[0].power = 8;
	hero[0].health = 20;
	
	// For hero 2 of 3: Mage
	strcpy(hero[1].class, "Mage");
	strcpy(hero[1].ability, "Ice Barrage");
	hero[1].power = 17;
	hero[1].health = 8;
	
	// For hero 3 of 3: Archer
	strcpy(hero[2].class, "Archer");
	strcpy(hero[2].ability, "Hurricane Shot");
	hero[2].power = 12;
	hero[2].health = 12;
	
	// Boss character: King Black Dragon
	struct character boss;
	
	strcpy(boss.class, "King Black Dragon");
	strcpy(boss.ability, "Fire Beam");
	boss.power = 25;
	boss.health = 30;
	
	// Entering a lucky number to decide srand
	srand(randomise());
	
	// While at least 1 hero and boss are both still alive, continue fighting
	int current_hero = 0;
	int round_counter = 1;
	while (still_alive(&boss, hero)) {
		// Cycle through to next hero if current one is defeated
		if (hero[current_hero].health <= 0) {
			current_hero++;
		}
		
		// Simultaneous attack!
		printf("*** Round %d! ***\n", round_counter);
		attack(&hero[current_hero], &boss);
		attack(&boss, &hero[current_hero]);
		printf("\n");
		
		round_counter++;
	}
	
	// End of fight
	end_fight(&boss);
	
	return 0;
}

// Lucky number that randomises attack values
int randomise(void){
	int lucky_number = 0;
	int looper = 1;
	while (looper) {
		printf("Enter a lucky number between 1 to 100: ");
		scanf("%d", &lucky_number);
		if (lucky_number >= 1 && lucky_number <= 100) {
			printf("\n");
			return lucky_number;
			looper = 0;
		} else {
			printf("You have entered an invalid input!\n");
		}
	}	
	return 0;
}

// Checks if boss both (individual) and anyone on team (hero array) is still alive
// If at least 1 alive on both sides, return 1
int still_alive(struct character *boss, struct character hero[TEAM_SIZE]) {
	// Is boss alive?
	int boss_alive = 0;
	if (boss->health > 0) {
		boss_alive = 1;
	}
	// Is anyone on the team alive?
	int team_alive = 0;
	int i = 0;
	while (i < TEAM_SIZE && !team_alive) {
		if (hero[i].health > 0) {
			team_alive = 1;
		}
		i++;
	}
	return boss_alive && team_alive;
}

// Attack function - deals damage to defender based on attacker's power
// Randomised based on lucky number input
void attack(struct character *attacker, struct character *defender) {
	// Reduce defender's health by random damage, based on attacker's power
	int damage = rand() % attacker->power;
	defender->health -= damage;
	// Prints the attack line 
	printf("%s used %s, dealing %d damage to %s!\n", 
		attacker->class, 
		attacker->ability, 
		damage, 
		defender->class
	);
	if (defender->health <= 0) {
		printf("%s has been defeated!\n", defender->class);
	}
}

// End of fight
void end_fight(struct character *boss) {
	printf("The battle has ended!\n");
	if (boss->health <= 0) {
		printf("The heroes are victorious! King Black Dragon has been defeated!\n");
	} else {
		printf("The heroes have been defeated. King Black Dragon triumphs today!\n");
	}
}
