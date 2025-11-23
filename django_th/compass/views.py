from django.shortcuts import render, redirect, get_object_or_404
from .models import Instruction
from .forms import InstructionForm


def compass_page(request):
    """
    Main compass view displaying the form to add instructions
    and a list of all existing instructions.
    """
    if request.method == 'POST':
        form = InstructionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('compass')
    else:
        form = InstructionForm()
    
    instructions = Instruction.objects.all().order_by('id')
    
    context = {
        'form': form,
        'instructions': instructions,
    }
    
    return render(request, 'compass/compass.html', context)


def instruction_detail(request, instruction_id):
    """
    Detail view for a specific instruction showing all details,
    including direction SVG and route summary.
    """
    instruction = get_object_or_404(Instruction, pk=instruction_id)
    summary = instruction.get_route_summary()
    
    context = {
        'instruction': instruction,
        'summary': summary,
    }
    
    return render(request, 'compass/instruction_detail.html', context)