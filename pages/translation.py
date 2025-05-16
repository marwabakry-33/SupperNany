from modeltranslation.translator import translator, TranslationOptions
from .models import AdviceBaby, AdviceMoon, AdviceBottel, AdviceBad, AdviceMother, Child, Task, HowTo

# لكل موديل فيهم حقل أو أكثر عايز تترجمها، تعرف TranslationOptions وتحدد الحقول اللي فيها نصوص

class AdviceBabyTranslationOptions(TranslationOptions):
    fields = ('advice_baby',)

class AdviceMoonTranslationOptions(TranslationOptions):
    fields = ('advice_baby',)

class AdviceBottelTranslationOptions(TranslationOptions):
    fields = ('advice_baby',)

class AdviceBadTranslationOptions(TranslationOptions):
    fields = ('advice_bad',)

class AdviceMotherTranslationOptions(TranslationOptions):
    fields = ('advice_mather',)

class ChildTranslationOptions(TranslationOptions):
    fields = ('baby', 'feedings', 'sleeping', 'Diapers',)

class TaskTranslationOptions(TranslationOptions):
    fields = ('content',)

class HowToTranslationOptions(TranslationOptions):
    fields = ('content',)

# سجل التعريفات في ال Translator
translator.register(AdviceBaby, AdviceBabyTranslationOptions)
translator.register(AdviceMoon, AdviceMoonTranslationOptions)
translator.register(AdviceBottel, AdviceBottelTranslationOptions)
translator.register(AdviceBad, AdviceBadTranslationOptions)
translator.register(AdviceMother, AdviceMotherTranslationOptions)
translator.register(Child, ChildTranslationOptions)
translator.register(Task, TaskTranslationOptions)
translator.register(HowTo, HowToTranslationOptions)
