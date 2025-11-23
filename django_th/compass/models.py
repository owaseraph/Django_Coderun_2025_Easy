from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Instruction(models.Model):
    """
    Model representing a treasure hunt instruction with direction, distance, 
    description, risk level, and link to previous instruction.
    """
    
    DIRECTION_CHOICES = [
        ('N', 'North'),
        ('S', 'South'),
        ('E', 'East'),
        ('W', 'West'),
        ('NE', 'North-East'),
        ('NW', 'North-West'),
        ('SE', 'South-East'),
        ('SW', 'South-West'),
    ]
    
    direction = models.CharField(
        max_length=2,
        choices=DIRECTION_CHOICES,
        help_text="Direction to travel"
    )
    
    distance = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Distance in nautical miles (must be greater than zero)"
    )
    
    description = models.TextField(
        help_text="Description of this instruction"
    )
    
    previous_instruction = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_instructions',
        help_text="Link to the previous instruction in the route"
    )
    
    risk_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Risk level (0-100) for the seas after this turn"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.id}: {self.distance} miles {self.get_direction_display()}"
    
    def get_route_summary(self):
        total_distance = self.distance
        total_risk = self.risk_level
        count = 1
        
        # Traverse forward through the route
        next_instructions = self.next_instructions.all()
        visited = {self.id}
        
        while next_instructions.exists():
            # Get all next instructions that haven't been visited
            unvisited = [inst for inst in next_instructions if inst.id not in visited]
            
            if not unvisited:
                break
            
            # Process first unvisited instruction (handles multiple routes)
            instruction = unvisited[0]
            visited.add(instruction.id)
            
            total_distance += instruction.distance
            total_risk += instruction.risk_level
            count += 1
            
            next_instructions = instruction.next_instructions.all()
        
        average_risk = total_risk / count if count > 0 else 0
        
        return {
            'total_distance': total_distance,
            'average_risk': round(average_risk, 2),
            'instruction_count': count
        }
