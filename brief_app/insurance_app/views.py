from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import UserProfile, Job, ContactMessage, Appointment
from .forms import UserProfileForm, UserSignupForm, ApplicationForm, ChangePasswordForm, PredictChargesForm,AppointmentForm
from django.http import HttpResponse
import pickle
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from django.views import View 
import pandas as pd
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from .models import Availability


#####Eliandy####

# Create your views here.
class HomeView(TemplateView):
    template_name = 'insurance_app/home.html'   # Home Page  View Template
         

class AboutView(TemplateView):
    template_name= 'insurance_app/about.html'   # About Us View Template


class JoinUsView(TemplateView):                
    template_name = 'insurance_app/join_us.html' # Join Us View Template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.all()
        return context


class ApplyView(TemplateView):                    # Team Apply View Template
    template_name = 'apply_thank_you.html'

    def post(self, request, *args, **kwargs):
        # Handle form submission here
        if request.method == 'POST':
            form = ApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                # Process the form (e.g., save data, send email, etc.)
                form.save()  # Save the application in our model 
                return redirect('apply_thank_you')  # Redirect to a thank you page
        else:
            form = ApplicationForm()
        
        return render(request, self.template_name, {'form': form})


# Logic to save the application data (e.g., store it in the database or email it)
def apply(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        job_id = request.POST.get('job_id')
        resume = request.FILES.get('resume')

        return HttpResponse("Application submitted successfully!")
    return redirect('join_us')

class HealthAdvicesView(TemplateView):
    template_name = 'insurance_app/health_advices.html'  # Assur'Cares Section View Template


class CybersecurityAwarenessView(TemplateView):
    template_name = 'insurance_app/cybersecurity_awareness.html'    # Cybersecurity Section View Template


#Welcome view (used to modified homepage)
class WelcomeView(TemplateView):
    template_name = 'insurance_app/welcome.html'  


#To handle the messages submission
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save the message to the database
        ContactMessage.objects.create(name=name, email=email, message=message)
        
        # Show a success message
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')  # Replace 'contact' with the name of your URL pattern
    
    return render(request, "insurance_app/contact_form.html")


# To see this messages 
@staff_member_required
def message_list_view(request):
    messages = ContactMessage.objects.all().order_by('-submitted_at')  # Most recent first
    return render(request, "insurance_app/messages_list.html", {"messages": messages})


# To solve the messages
@csrf_exempt
def solve_message(request, message_id):
    if request.method == 'POST':
        try:
            contact_message = ContactMessage.objects.get(id=message_id)
            contact_message.delete()
            return JsonResponse({'success': True})
        except ContactMessage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Message not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


# Dynamic quote :
def predict_charges(request):
    prediction = None

    # Handle the GET request - Render the form
    if request.method == 'GET':
        return render(request, 'insurance_app/insurance_form.html', {'prediction': prediction})

    # Handle the POST request - Process the form data and predict
    elif request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Extract data from the JSON
            height = float(data.get('height'))
            weight = float(data.get('weight'))
            age = int(data.get('age'))
            sex = data.get('sex')
            smoker = data.get('smoker')
            region = data.get('region')
            children = int(data.get('children'))
            bmi = float(data.get('bmi'))
            bmi_category = data.get('bmi_category')

            # Load model from pickle
            model_path = 'insurance_app/model/model_1.pickle'
            with open(model_path, 'rb') as file:
                model = pickle.load(file)

            # Prepare data as a DataFrame (ensure the order matches your model's expected input)
            input_data = pd.DataFrame([{
                'height': height,
                'weight': weight,
                'age': age,
                'sex': sex,
                'smoker': smoker,
                'region': region,
                'children': children,
                'bmi': bmi,
                'BMI_category': bmi_category
            }])

            # Make the prediction
            prediction = round(model.predict(input_data)[0], 2)

            # Ensure prediction is non-negative
            prediction = max(prediction, 0)

            # Return prediction as JSON response
            return JsonResponse({'prediction': prediction})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # If not GET or POST, return an error
    return JsonResponse({'error': 'Invalid request method'}, status=405)





#Admin view for appointments
@staff_member_required
def admin_appointment_list(request):
    """Show upcoming and past appointments for admins."""
    appointments = Appointment.objects.all().order_by('date')
    future_appointments = appointments.filter(date__gte=now())
    past_appointments = appointments.filter(date__lt=now())

    return render(request, 'insurance_app/appointments/admin_appointment_list.html', {
        'future_appointments': future_appointments,
        'past_appointments': past_appointments
    })


class SignupView(CreateView):                           # Generic view for creating an object
    model = UserProfile                                 # Model used
    form_class = UserSignupForm                         # Form used
    template_name = 'insurance_app/signup.html'         # HTML template for displaying the form
    success_url = reverse_lazy('login')  

class CustomLoginView(LoginView):
    template_name = 'insurance_app/login.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        # Redirect to the profile page after successful login
        return reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to the profile page
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)


# Template for user profile view
class UserProfileView(LoginRequiredMixin, UpdateView): 
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'insurance_app/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Return the UserProfile object for the logged-in user
        print(self.request.user)
        return self.request.user
    
    def form_valid(self, form):
            # Save the form and display a success message
            response = super().form_valid(form)
            messages.success(self.request, 'Your profile has been updated!')
            return response


class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm  
    template_name = 'insurance_app/changepassword.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        # Save the new password
        response = super().form_valid(form)
        # Add a success message
        messages.success(self.request, 'Your password has been changed successfully!')
        return response
    

class PredictChargesView(LoginRequiredMixin, UpdateView): 
    model = get_user_model()
    form_class = PredictChargesForm
    template_name = 'insurance_app/predict.html'
    success_url = reverse_lazy('predict')

    def get_object(self, queryset=None):
        # Return the UserProfile object for the logged-in user
        print(self.request.user)
        return self.request.user
    
    def form_valid(self, form):
            # Save the form and display a success message
            response = super().form_valid(form)
            messages.success(self.request, 'Your charges has been updated!')
            return response


class UserLogoutView(LoginRequiredMixin, View):
    template_name = 'insurance_app/logout_user.html'
    next_page = reverse_lazy('logout_user')

    def get(self, request):
        # Handle GET requests with confirmation page
        user = self.request.user
        return render(request, self.template_name, {'user': user})
    
    def post(self, request):
        # Handle actual logout
        user = self.request.user
        logout(request)
        return render(request, self.template_name, {'user': user})
    
    
# class PredictChargesView(LoginRequiredMixin, UpdateView):
#     model = UserProfile  # Specify the model to work with
#     form_class = PredictChargesForm  # Use your custom form
#     template_name = 'insurance_app/predict.html'  # Template for rendering the form
#     success_url = reverse_lazy('predict')  # URL to redirect to after successful form submission

#     def get_object(self, queryset = None):
#         return self.request.user

#     def form_valid(self, form):
#         user_profile = self.get_object()

#         # Update values from form
#         user_profile.age = form.cleaned_data.get('age')
#         user_profile.weight = form.cleaned_data.get('weight')
#         user_profile.height = form.cleaned_data.get('height')
#         user_profile.num_children = form.cleaned_data.get('num_children')
#         user_profile.smoker = form.cleaned_data.get('smoker')
#         # user_profile.save()  # Save updated profile data

#         if user_profile.weight is None or user_profile.height is None or user_profile.height == 0:
#             return render(self.request, self.template_name, {
#                 "error": "Invalid weight or height values.",
#                 "form": form
#             })

#         # Calculate BMI
#         bmi = user_profile.weight / ((user_profile.height / 100) ** 2)

#         personal_data = {
#             "age": user_profile.age,
#             "bmi": bmi,
#             "smoker": user_profile.smoker,
#             "children": user_profile.num_children,
#         }

#         # Preprocess the data
#         preprocessed_data = self.preprocess_data(personal_data)

#         print("Preprocessed Data:", preprocessed_data)  # Debugging

#         # Load the model
#         model = self.load_model()
#         if model is None:
#             return render(self.request, self.template_name, {
#                 "error": "Failed to load the model.",
#                 "form": form
#             })

#         # Predict charges
#         predicted_charges = model.predict(preprocessed_data)
#         print("Predicted Charges:", predicted_charges)  # Debugging

#         return render(self.request, self.template_name, {
#             "predicted_charges": round(predicted_charges[0], 2),
#             "form": form
#         })
    
#     def categorize_bmi(self, bmi):
#         if bmi < 18.5:
#             return "under_weight"
#         elif 18.5 <= bmi < 25:
#             return "normal_weight"
#         elif 25 <= bmi < 30:
#             return "over_weight"
#         else:
#             return "obese"

#     def categorize_age(self, age):
#         if 18 < age < 26:
#             return "young_adult"
#         elif 26 <= age < 36:
#             return "early_adulthood"
#         elif 36 <= age < 46:
#             return "mid_adulthood"
#         else:
#             return "late_adulthood"

#     def preprocess_data(self, data):
#         # Define the expected columns (must match the model's input requirements)
#         expected_columns = [
#             "smoker",
#             "age",
#             "bmi",
#             "age_category_young_adult",
#             "age_category_early_adulthood",
#             "bmi_category_over_weight",
#             "bmi_category_obese",
#             "children_str_0",
#         ]

#         # Create a DataFrame from the input data
#         df = pd.DataFrame([data])

#         # Convert smoker to binary (1 for "Yes", 0 for "No")
#         df["smoker"] = df["smoker"].map({"Yes": 1, "No": 0})

#         # Categorize age and bmi
#         df["age_category"] = df["age"].apply(self.categorize_age)
#         df["bmi_category"] = df["bmi"].apply(self.categorize_bmi)

#         # Convert children to string (for one-hot encoding)
#         df["children_str"] = df["children"].apply(lambda x: str(x))

#         # Perform one-hot encoding for categorical columns
#         df = pd.get_dummies(df, columns=["age_category", "bmi_category", "children_str"], dtype=(int))

#         # Ensure all expected columns are present
#         for col in expected_columns:
#             if col not in df.columns:
#                 df[col] = 0  # Add missing columns with default value 0

#         # Reorder columns to match the model's expectations
#         df = df[expected_columns]

#         # Debugging: Print the final preprocessed DataFrame
#         print("Final Preprocessed DataFrame:")
#         print(df)

#         return df

#     def load_model(self):
#         try:
#             model_path = os.path.join(settings.BASE_DIR, 'insurance_app/model/model.pkl')
#             with open(model_path, "rb") as file:
#                 model = pickle.load(file)
#             return model
#         except FileNotFoundError:
#             print("Error: The model file 'model.pkl' was not found.")
#             return None
#         except pickle.UnpicklingError:
#             print("Error: The file could not be unpickled. Ensure it is a valid pickle file.")
#             return None
        
    # def get_context_data(self, **kwargs):
    #     # Add the predicted charges to the context (if available)
    #     context = super().get_context_data(**kwargs)
    #     if hasattr(self, 'predicted_charges'):
    #         context['predicted_charges'] = self.predicted_charges
    #     return context
    
    # def form_valid(self, form):
    #     # Fetch the user's profile data
    #     user_profile = self.get_object()

    #     # Prepare input data for the model
    #     age = form.cleaned_data['age']
    #     bmi = form.cleaned_data['weight'] / ((form.cleaned_data['height'] / 100) ** 2)  # Calculate BMI
    #     children = form.cleaned_data['num_children']
    #     smoker = form.cleaned_data['smoker']

    #     personal_data = {"age": age, "bmi": bmi, "smoker": smoker, "children": children}

    #     # Preprocess the data
    #     preprocessed_data = self.preprocess_data(personal_data)

    #     # Debugging: Print the preprocessed data
    #     print("Preprocessed Data:")
    #     print(preprocessed_data)

    #     # Load the model
    #     model = self.load_model()
    #     if model is None:
    #         return render(self.request, self.template_name, {"error": "Failed to load the model.", "form": form})

    #     # Predict charges
    #     predicted_charges = model.predict(preprocessed_data)

    #     # Debugging: Print the predicted charges
    #     print("Predicted Charges:")
    #     print(predicted_charges)

    #     # Store the predicted charges in the instance for use in the template
    #     self.predicted_charges = round(predicted_charges[0], 2)

    #     # Render the template with the predicted charges and updated form
    #     return self.render_to_response(self.get_context_data(form=form))







#################################################################################


    # class SignupView(CreateView):
#     model = UserProfile
#     form_class = UserSignupForm  # Utilisez un formulaire personnalisé
#     template_name = 'insurance_app/signup.html'
#     success_url = reverse_lazy('login')
#     # redirect_authenticated_user = True  # Redirect already logged-in users

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.set_password(form.cleaned_data['password'])
#         user.save()
#         return super().form_valid(form)

# class CustomLoginView(LoginView):
#     template_name = 'insurance_app/login.html' 
#     success_url = reverse_lazy('profile')
#     def form_valid(self, form):
#         # Authenticate the user
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(self.request, username=username, password=password)

#         if user is not None:
#             # Log in the user and redirect
#             login(self.request, user)
#             return super().form_valid(form)
#         else:
#             # Invalid credentials, show error message
#             form.add_error(None, 'Invalid username or password.') # Add a general error message
#             return self.form_invalid(form)