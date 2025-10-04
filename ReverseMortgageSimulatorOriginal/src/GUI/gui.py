from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.core.window import Window
import sys
sys.path.append("src")

# Reverse Mortgage logic
from ReverseMortgage import MonthlyPayment

class EmptyInput(Exception):
    pass

class ReverseMortgageApp(App):
    def build(self):
        """
        Main method that initializes the application by creating the GUI layouts.
        """
        Window.clearcolor = (0.1,0.1,0.2,0)
        self.client_layout = self.create_client_information_layout()
        self.property_layout = self.create_property_information_layout()
        self.inputs_layout = self.create_inputs_layout(self.client_layout, self.property_layout)
        self.global_layout = self.create_global_layout(self.inputs_layout)
        
        return self.global_layout

    def create_client_information_layout(self):
        """
        Creates and returns the layout for collecting client information.
        """
        layout = GridLayout(cols=2, spacing=10)

        self.age_label = Label(text="Age *", size_hint=(0.5, 0.15), font_size=20)
        layout.add_widget(self.age_label)
        self.age_input = TextInput(multiline=False, size_hint=(0.5, 0.15), input_filter="int", text='0')
        layout.add_widget(self.age_input)
        self.age_input.bind(text=self.check_valid_age)

        self.gender_label = Label(text="Gender *", size_hint=(0.5, 0.15), font_size=20)
        layout.add_widget(self.gender_label)
        self.gender_spinner = Spinner(text="Select", values=('M', 'F'), size_hint=(0.5, 0.15))
        layout.add_widget(self.gender_spinner)
        self.gender_spinner.bind(text=self.check_valid_spinner)

        self.marital_status_label = Label(text="Marital Status *", size_hint=(0.5, 0.15), font_size=20)
        layout.add_widget(self.marital_status_label)
        self.marital_status_spinner = Spinner(text="Select", values=('Married', 'Single', 'Widowed', 'Divorced'), size_hint=(0.5, 0.15))
        layout.add_widget(self.marital_status_spinner)
        self.marital_status_spinner.bind(text=self.update_spouse_fields)
        self.marital_status_spinner.bind(text=self.check_valid_spinner)

        # Placeholder for spouse fields
        self.spouse_age_input = Label(text='None')
        self.spouse_gender_spinner = Label(text='None')
        self.is_married = False

        return layout

    def create_property_information_layout(self):
        """
        Creates and returns the layout for collecting property information.
        """
        layout = GridLayout(cols=2)

        self.property_value_label = Label(text="Property Value", size_hint=(0.5, 0.1), font_size=20)
        layout.add_widget(self.property_value_label)
        self.property_value_input = TextInput(multiline=False, size_hint=(0.5, 0.1), input_filter="int", text='0')
        layout.add_widget(self.property_value_input)

        self.interest_rate_label = Label(text="Interest Rate", size_hint=(0.5, 0.1), font_size=20)
        layout.add_widget(self.interest_rate_label)
        self.interest_rate_input = TextInput(multiline=False, size_hint=(0.5, 0.1), input_filter="float", text='0')
        layout.add_widget(self.interest_rate_input)

        return layout

    def create_inputs_layout(self, client_layout, property_layout):
        """
        Combines the client and property information layouts into a horizontal layout.
        """
        layout = BoxLayout(orientation="horizontal", padding=15, spacing=10)
        layout.add_widget(client_layout)
        layout.add_widget(property_layout)
        return layout

    def create_global_layout(self, inputs_layout):
        """
        Creates the global layout, which includes the input forms and the calculation button.
        """
        layout = GridLayout(rows=3, padding=15, spacing=10)

        layout.add_widget(Label(text="Reverse Mortgage Calculator", size_hint=(1, 0.1), halign="center", font_family="Arial", font_size=30))
        layout.add_widget(inputs_layout)

        self.calc_button = Button(text="Calculate", size_hint=(0.5, 0.1), background_color=[0,0,0,1])
        layout.add_widget(self.calc_button)
        self.calc_button.bind(on_press=self.calculate_reverse_mortgage)

        return layout

    def update_spouse_fields(self, sender, text):
        """
        Updates the form when the marital status is set to 'Married', showing additional fields.
        """
        if text == 'Married' and not self.is_married:
            self.spouse_age_label = Label(text="Spouse's Age *", size_hint=(0.5, 0.15), font_size=20)
            self.client_layout.add_widget(self.spouse_age_label)

            self.spouse_age_input = TextInput(multiline=False, size_hint=(0.5, 0.15), input_filter="int", text='0')
            self.client_layout.add_widget(self.spouse_age_input)
            self.spouse_age_input.bind(text=self.check_valid_age)

            self.spouse_gender_label = Label(text="Spouse's Gender *", size_hint=(0.5, 0.15), font_size=20)
            self.client_layout.add_widget(self.spouse_gender_label)

            self.spouse_gender_spinner = Spinner(text="Select", values=('M', 'F'), size_hint=(0.5, 0.15))
            self.client_layout.add_widget(self.spouse_gender_spinner)

            self.is_married = True
        elif text != 'Married' and self.is_married:
            self.client_layout.remove_widget(self.spouse_age_input)
            self.client_layout.remove_widget(self.spouse_age_label)
            self.client_layout.remove_widget(self.spouse_gender_label)
            self.client_layout.remove_widget(self.spouse_gender_spinner)
            self.is_married = False

    def check_valid_age(self, sender, text):
        """
        Validates the age input to ensure it's within a valid range (0-100).
        """
        if sender is self.age_input:
            if (text != '' and text != '-') and (int(text) < 0 or int(text) > 100):
                self.age_label.text = "Age *"
            elif text == '' or text == '-':
                self.age_label.text = "Age *"
            else:
                self.age_label.text = "Age"
        elif sender is self.spouse_age_input:
            if (text != '' and text != '-') and (int(text) < 0 or int(text) > 100):
                self.spouse_age_label.text = "Spouse's Age *"
            elif text == '' or text == '-':
                self.spouse_age_label.text = "Spouse's Age *"
            else:
                self.spouse_age_label.text = "Spouse's Age"

    def check_valid_spinner(self, sender, text):
        """
        Checks that the Spinner values are correctly set (not 'Select').
        """
        if text != 'Select' and sender is self.gender_spinner:
            self.gender_label.text = 'Gender'
        elif text != 'Select' and sender is self.spouse_gender_spinner:
            self.spouse_gender_label = 'Spouse\'s Gender'
        elif text != 'Select' and sender is self.marital_status_spinner:
            self.marital_status_label.text = 'Marital Status'

    def calculate_reverse_mortgage(self, sender):
        """
        Calculates the reverse mortgage when the button is pressed and displays a result or error message.
        """
        try:
            for layout in self.inputs_layout.children:
                for child in layout.children:
                    if isinstance(child, TextInput) and child.text == "":
                        raise EmptyInput(f"There's an empty input. Please verify the information")
                
            if self.is_married:
                client = MonthlyPayment.Client(int(self.age_input.text), self.gender_spinner.text, self.marital_status_spinner.text, int(self.spouse_age_input.text), self.spouse_gender_spinner.text)
            else:
                client = MonthlyPayment.Client(int(self.age_input.text), self.gender_spinner.text, self.marital_status_spinner.text, None, None)

            reverse_mortgage = MonthlyPayment.ReverseMortgage(int(self.property_value_input.text), float(self.interest_rate_input.text), client)

            popup = Popup(title = 'Reverse Mortgage Calculated Successfully', content = Label(text = f'{reverse_mortgage}'), size_hint = (0.8, 0.4))
            popup.content.bind(on_touch_down=popup.dismiss)
            popup.open()
        except (MonthlyPayment.ClientException, MonthlyPayment.ReverseMortgageException, EmptyInput) as e:
            popup = Popup(title = 'Error', content = Label(text = f'{e}'), size_hint = (0.8, 0.4))
            popup.content.bind(on_touch_down=popup.dismiss)
            popup.open()

if __name__ == "__main__":
    ReverseMortgageApp().run()
