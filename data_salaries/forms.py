from django import forms

class upload_file(forms.Form):
    upload_file = forms.FileField(label='Base de datos')

experience_level_opt = {'MI': 'MI','SE': 'SE','EN': 'EN','EX': 'EX'}

employment_type_opt = {'FT': 'FT','CT': 'CT','PT': 'PT','FL': 'FL'}

employee_residence_opt = {
    'AU': 'AU', 'US': 'US', 'GB': 'GB', 'CA': 'CA', 'NL': 'NL', 'LT': 'LT', 'DK': 'DK', 'FR': 'FR',
    'ZA': 'ZA', 'NZ': 'NZ', 'AR': 'AR', 'ES': 'ES', 'KE': 'KE', 'LV': 'LV', 'GE': 'GE', 'IN': 'IN',
    'DE': 'DE', 'IL': 'IL', 'FI': 'FI', 'AT': 'AT', 'HR': 'HR', 'BR': 'BR', 'CH': 'CH', 'AE': 'AE',
    'GR': 'GR', 'PL': 'PL', 'SA': 'SA', 'UA': 'UA', 'EG': 'EG', 'PH': 'PH', 'TR': 'TR', 'OM': 'OM',
    'MX': 'MX', 'PT': 'PT', 'BA': 'BA', 'IT': 'IT', 'IE': 'IE', 'EE': 'EE', 'MT': 'MT', 'LB': 'LB',
    'RO': 'RO', 'HU': 'HU', 'VN': 'VN', 'NG': 'NG', 'CZ': 'CZ', 'PK': 'PK', 'UG': 'UG', 'CO': 'CO',
    'SI': 'SI', 'MU': 'MU', 'AM': 'AM', 'TH': 'TH', 'KR': 'KR', 'QA': 'QA', 'RU': 'RU', 'TN': 'TN',
    'GH': 'GH', 'BE': 'BE', 'AD': 'AD', 'EC': 'EC', 'PE': 'PE', 'MD': 'MD', 'NO': 'NO', 'UZ': 'UZ',
    'JP': 'JP', 'HK': 'HK', 'CF': 'CF', 'SG': 'SG', 'SE': 'SE', 'KW': 'KW', 'CY': 'CY', 'IR': 'IR',
    'AS': 'AS', 'CN': 'CN', 'CR': 'CR', 'CL': 'CL', 'PR': 'PR', 'BO': 'BO', 'DO': 'DO', 'ID': 'ID',
    'MY': 'MY', 'HN': 'HN', 'DZ': 'DZ', 'IQ': 'IQ', 'BG': 'BG', 'JE': 'JE', 'RS': 'RS', 'LU': 'LU'
}

remote_ratio_opt = {'0': '0','50': '50','100': '100'}

company_location_opt = {
    'AU': 'AU', 'US': 'US', 'GB': 'GB', 'CA': 'CA', 'NL': 'NL', 'LT': 'LT', 'DK': 'DK', 'FR': 'FR',
    'ZA': 'ZA', 'NZ': 'NZ', 'AR': 'AR', 'ES': 'ES', 'KE': 'KE', 'LVIN': 'LVIN', 'DE': 'DE', 'IL': 'IL',
    'FI': 'FI', 'AT': 'AT', 'BR': 'BR', 'CH': 'CH', 'AE': 'AE', 'PL': 'PL', 'SA': 'SA', 'UA': 'UA',
    'EG': 'EG', 'PH': 'PH', 'TR': 'TR', 'OM': 'OM', 'MX': 'MX', 'PT': 'PT', 'BA': 'BA', 'IT': 'IT',
    'AS': 'AS', 'IE': 'IE', 'EE': 'EE', 'MT': 'MT', 'HU': 'HU', 'LB': 'LB', 'RO': 'RO', 'VN': 'VN',
    'NG': 'NG', 'LU': 'LU', 'GI': 'GI', 'CO': 'CO', 'SI': 'SI', 'GR': 'GR', 'MU': 'MU', 'RU': 'RU',
    'KR': 'KR', 'CZ': 'CZ', 'QA': 'QA', 'GH': 'GH', 'SE': 'SE', 'AD': 'AD', 'EC': 'EC', 'NO': 'NO',
    'JP': 'JP', 'HK': 'HK', 'CF': 'CF', 'SG': 'SG', 'TH': 'TH', 'HR': 'HR', 'AM': 'AM', 'PK': 'PK',
    'IR': 'IR', 'BS': 'BS', 'PR': 'PR', 'BE': 'BE', 'ID': 'ID', 'MY': 'MY', 'HN': 'HN', 'DZ': 'DZ',
    'IQ': 'IQ', 'CN': 'CN', 'CL': 'CL', 'MD': 'MD'
    }

company_size_opt = {'S': 'S','M': 'M','L': 'L'}

class view_filter(forms.Form):
    experience_level = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=experience_level_opt,
        )
    
    employment_type = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=employment_type_opt,
        )
    
    employee_residence = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=employee_residence_opt,
        )
    
    remote_ratio = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=remote_ratio_opt,
        )
    
    company_location = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=company_location_opt,
        )
    
    company_size = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=company_size_opt,
        )
    
vars_opt = {
    'experience_level': 'experience_level', 'employment_type': 'employment_type',
    'employee_residence': 'employee_residence', 'remote_ratio': 'remote_ratio',
    'company_location': 'company_location', 'company_size': 'company_size'
} 

class analize_filter(forms.Form):
    filter_vars = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=vars_opt
    )