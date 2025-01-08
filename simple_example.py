from dataclasses import dataclass
from typing import List, Callable, Optional
import random
from openai import OpenAI
import numpy as np

@dataclass
class Idea:
    """Represents a generated idea with its fitness score."""
    content: str
    score: float = 0.0
    parent: Optional['Idea'] = None
    
class CreativeExplorer:
    def __init__(
        self, 
        client: OpenAI,
        fitness_fn: Callable[[str], float],
        population_size: int = 5,
        mutation_rate: float = 0.3
    ):
        self.client = client
        self.fitness_fn = fitness_fn
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population: List[Idea] = []
        
    def generate_initial_population(self, prompt: str) -> List[Idea]:
        """Generate initial population of ideas using the LLM."""
        messages = [
            {"role": "system", "content": "You are a creative assistant generating diverse ideas."},
            {"role": "user", "content": f"Generate a unique response to: {prompt}"}
        ]
        
        population = []
        for _ in range(self.population_size):
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.9  # High temperature for diversity
            )
            content = response.choices[0].message.content
            idea = Idea(content=content)
            population.append(idea)
            
        return population
    
    def evaluate_population(self, population: List[Idea]) -> List[Idea]:
        """Score each idea using the fitness function."""
        for idea in population:
            idea.score = self.fitness_fn(idea.content)
        return sorted(population, key=lambda x: x.score, reverse=True)
    
    def mutate(self, idea: Idea) -> Idea:
        """Generate a mutation of an idea using the LLM."""
        messages = [
            {"role": "system", "content": "You are a creative assistant generating variations of ideas."},
            {"role": "user", "content": f"Generate a creative variation of this idea: {idea.content}"}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=self.mutation_rate
        )
        
        return Idea(
            content=response.choices[0].message.content,
            parent=idea
        )
    
    def evolve_population(self, population: List[Idea]) -> List[Idea]:
        """Create next generation through mutation and selection."""
        # Keep top performers
        next_gen = population[:2]
        
        # Generate mutations from top performers
        while len(next_gen) < self.population_size:
            parent = random.choice(population[:2])
            mutation = self.mutate(parent)
            next_gen.append(mutation)
            
        return next_gen
    
    def explore(self, prompt: str, generations: int = 3) -> List[Idea]:
        """Main exploration loop."""
        # Generate initial population
        self.population = self.generate_initial_population(prompt)
        
        for generation in range(generations):
            # Evaluate current population
            self.population = self.evaluate_population(self.population)
            
            # Evolve to next generation
            self.population = self.evolve_population(self.population)
            
        # Final evaluation
        return self.evaluate_population(self.population)

# Example usage and testing code
def simple_fitness_function(text: str) -> float:
    """A simple fitness function based on text length and uniqueness."""
    # This is a placeholder - replace with your own criteria
    unique_words = len(set(text.lower().split()))
    total_words = len(text.split())
    return unique_words / total_words if total_words > 0 else 0

def run_example():
    client = OpenAI()  # Replace with your API key setup
    
    explorer = CreativeExplorer(
        client=client,
        fitness_fn=simple_fitness_function,
        population_size=5,
        mutation_rate=0.3
    )
    
    prompt = "Describe a novel transportation system for a future city"
    results = explorer.explore(prompt, generations=3)
    
    # Print results
    for i, idea in enumerate(results):
        print(f"\nIdea {i+1} (Score: {idea.score:.2f}):")
        print(idea.content)
        print("-" * 50)

if __name__ == "__main__":
    run_example()