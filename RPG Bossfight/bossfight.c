// A simulation of 3 heroes fighting a boss in an RPG
// Created on 01/08/2020 by Stanford Lee
//
// User inputs a 'lucky number', and then simulation is executed
// Heroes and boss attack simultaneously - if hero is defeated, switch to next hero

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define TEAM_SIZE 3
#define MAX_LENGTH 100
#define LUCKY_NUMBER_START 1
#define LUCKY_NUMBER_END 8

// Creating struct for character, used for both adventurer and boss
struct character {
	char class[MAX_LENGTH];
	char ability[MAX_LENGTH];
	int power;
	int health;
};

void create_chars(struct character *boss, struct character hero[TEAM_SIZE]);
int introduction(void);
int randomise(void);
int still_alive(struct character *boss, struct character hero[TEAM_SIZE]);
void attack(struct character *attacker, struct character *defender);
void battle(struct character *boss, struct character hero[TEAM_SIZE]);
void end_fight(struct character *boss);

int main (void) {

    // Create character structs
    struct character hero[TEAM_SIZE];
    struct character boss;

    // Create individual character attributes
    create_chars(&boss, hero);
	
    // Provide text introduction to the game
    introduction();

	// Entering a lucky number to decide srand, which impacts damage dealt
	srand(randomise());
	
	// While at least 1 hero and boss are both still alive, continue fighting
	battle(&boss, hero);

	// End of fight, print victory/defeat message
	end_fight(&boss);

	return 0;
}

// Create structs for heroes and enemy boss character
void create_chars(struct character *boss, struct character hero[TEAM_SIZE]){
	// Hero character array
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
	strcpy(boss->class, "King Black Dragon");
	strcpy(boss->ability, "Fire Beam");
	boss->power = 25;
	boss->health = 30;
}

// Text-based narrative introduction to the game
int introduction(void){
    printf("\nThe band of adventurers finally reach the end of the lava maze and are faced with an ashen expanse.\n");
    printf("They hear a thunderous roar that trembles the charred ground beneath them. They steel themselves for the final battle.\n");
    printf("The King Black Dragon emerges from the flames.\n");
    printf("\nThe heroes recall that there were 8 magic symbols inscribed at the entrance of the maze.");
    printf("One of these was the key to defeating the dragon, but they did not know which one.\n");
    printf("The dragon reared its armoured head and fixated its terrifying gaze on the three heroes, ready to strike.\n");
    return 0;
}

// Lucky number that randomises attack values
int randomise(void){
	int lucky_number = 0;
	int looper = 1;
	while (looper) {
		printf("\nWhich symbol should the adventurers choose?\n");
        printf("[Enter a number between 1 to 8]: ");
		scanf("%d", &lucky_number);
		if (lucky_number >= LUCKY_NUMBER_START && lucky_number <= LUCKY_NUMBER_END) {
			printf("\nThe adventurers chose the number %d!\n", lucky_number);
            printf("[Press ENTER to continue]\n");
            while(getchar()!='\n');
            while(getchar()!='\n');
			return lucky_number;
			looper = 0;
		} else {
			printf("\nThere were %d symbols. Enter another number!\n", LUCKY_NUMBER_END);
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

// Triggers battle between characters by calling check and attack functions
void battle(struct character *boss, struct character hero[TEAM_SIZE]){
    int current_hero = 0;
	int round_counter = 1;
	while (still_alive(boss, hero)) {
		// Cycle through to next hero if current one is defeated
		if (hero[current_hero].health <= 0) {
			current_hero++;
		}
		
		// Simultaneous attack!
		printf("*** Round %d! ***\n", round_counter);
		attack(&hero[current_hero], boss);
		attack(boss, &hero[current_hero]);
		
		round_counter++;
        printf("[Press ENTER to continue]\n");
        while(getchar()!='\n');
	}
}

// End of fight
void end_fight(struct character *boss) {
	printf("The battle has ended!\n\n");
	if (boss->health <= 0) {
        printf("Imbued with the power of the ancient spirits, the heroes resist defeat and vanquish their foe!\n");
        printf("The magic symbol the heroes selected was the right one!\n");
		printf("\nThe heroes are victorious! King Black Dragon has been defeated, and his legend is put to rest forever!\n");
	} else {
        printf("Unfortunately, the magic symbol the heroes selected was ineffective!\n");
        printf("Without the ancient spell, the heroes faced an impossible opponent.\n");
		printf("\nThe heroes have been defeated and have failed in their quest. King Black Dragon triumphs today!\n");
	}
}