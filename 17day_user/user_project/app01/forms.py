from django import forms
from .models import PrettyNum
import re

class PrettyNumModelForm(forms.ModelForm):
    # 重写手机号，最小11位
    mobile = forms.CharField(
        label="手机号码",
        min_length=11,
        max_length=11
    )

    class Meta:
        model = PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 统一加上bootstrap样式
        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"form-control","placeholder":field.label})

    def clean_mobile(self):
        """自定义校验手机号正则"""
        num = self.cleaned_data.get("mobile")
        if not re.match(r'^1[3-9]\d{9}$', num):
            raise forms.ValidationError("手机号格式不正确！")
        return num