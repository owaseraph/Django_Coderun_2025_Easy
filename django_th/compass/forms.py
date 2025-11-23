from django import forms
from django.core.exceptions import ValidationError
from .models import Instruction


class InstructionForm(forms.ModelForm):
    
    class Meta:
        model = Instruction
        fields = ['direction', 'distance', 'description', 'previous_instruction', 'risk_level']
        widgets = {
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'distance': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Enter distance in nautical miles'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter instruction description'
            }),
            'previous_instruction': forms.Select(attrs={'class': 'form-control'}),
            'risk_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'placeholder': 'Enter risk level (0-100)'
            }),
        }
        labels = {
            'direction': 'Direction',
            'distance': 'Distance (nautical miles)',
            'description': 'Description',
            'previous_instruction': 'Previous Instruction (optional)',
            'risk_level': 'Risk Level (0-100)',
        }
    
    def clean_distance(self):
        """Validate that distance is greater than zero."""
        distance = self.cleaned_data.get('distance')
        if distance is not None and distance <= 0:
            raise ValidationError('Distance must be greater than zero.')
        return distance
    
    def clean_description(self):
        """Validate that description is not empty."""
        description = self.cleaned_data.get('description')
        if description is not None and not description.strip():
            raise ValidationError('Description cannot be empty.')
        return description.strip()
    
    def clean_risk_level(self):
        """Validate that risk level is between 0 and 100."""
        risk_level = self.cleaned_data.get('risk_level')
        if risk_level is not None:
            if risk_level < 0 or risk_level > 100:
                raise ValidationError('Risk level must be between 0 and 100.')
        return risk_level
    
    def clean(self):
        """Additional validation to prevent circular references."""
        cleaned_data = super().clean()
        previous_instruction = cleaned_data.get('previous_instruction')
        
        # If this is an update (instance exists), check for circular references
        if self.instance.pk and previous_instruction:
            # Check if the previous instruction would create a cycle
            current = previous_instruction
            visited = {self.instance.pk}
            
            while current:
                if current.pk in visited:
                    raise ValidationError({
                        'previous_instruction': 'Cannot create circular reference in instruction chain.'
                    })
                visited.add(current.pk)
                current = current.previous_instruction
        
        return cleaned_data
