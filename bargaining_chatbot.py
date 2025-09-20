#!/usr/bin/env python3
import time
import random

class BargainingChatbot:
    """
    An AI-powered bargaining chatbot for an artisan marketplace.
    This class simulates negotiation, translation, and discount application.
    """
    def __init__(self, product_name, ideal_price, min_price, customer_language, seller_language):
        """
        Initializes the chatbot with product details and negotiation parameters.
        
        Args:
            product_name (str): The name of the product.
            ideal_price (float): The seller's ideal selling price.
            min_price (float): The minimum price the seller will accept.
            customer_language (str): The customer's language code (e.g., 'en', 'te', 'hi').
            seller_language (str): The seller's language code.
        """
        self.product_name = product_name
        self.ideal_price = float(ideal_price)
        self.min_price = float(min_price)
        self.current_price = self.ideal_price
        self.customer_language = customer_language
        self.seller_language = seller_language
        self.loyalty_points = 0  # Placeholder for loyalty points
        self.discounts = {
            "festival": 0.10,  # 10% discount for a festival
            "loyalty": 0.05    # 5% discount for loyalty points
        }
        self.is_accepted = False
        self.translations = {
            "en": {
                "welcome": "Hello! I am the AI bargaining assistant for this beautiful {}. What is your offer?",
                "original_price": "The original price for this {} is ₹{:.0f}. What is your first offer?",
                "offer_accepted": "Excellent! We have a deal. The final price is ₹{:.0f}.",
                "goodbye": "Thank you for your interest! Have a wonderful day!",
                "discount_applied": "Based on our ongoing festival offer, an additional {}% discount has been applied!",
                "loyalty_discount": "Thank you for being a loyal customer! An additional {}% discount has been applied for your loyalty points!",
                "current_price": "The current price for the {} is ₹{:.0f}. What's your next offer?",
                "invalid_price": "Please enter a valid price.",
                "seller_offer_received": "Seller: Customer's offer received: ₹{:.0f}",
                "offer_too_low_options": [
                    "That offer is too low. Please try again with a higher offer.",
                    "We can't accept that. Our minimum price is higher than your offer. Please try again.",
                    "Your offer is too low to be considered. What's your next price?",
                    "I'm sorry, but that is below our lowest acceptable price. Please increase your offer."
                ],
                "counter_offer_options": [
                    "Thank you for your offer of ₹{:.0f}. That is a bit low. How about we meet in the middle at ₹{:.0f}?",
                    "That's a good start, but it's not quite what we had in mind. Let's try to meet in the middle at ₹{:.0f}.",
                    "I appreciate your offer of ₹{:.0f}. Let's split the difference. I can accept ₹{:.0f}.",
                    "I cannot accept that price. However, I can offer you a counter-price of ₹{:.0f}."
                ]
            },
            "te": {
                "welcome": "నమస్కారం! నేను ఈ అందమైన {} కోసం AI బేరసారాల సహాయకుడిని. మీ ఆఫర్ ఏమిటి?",
                "original_price": "ఈ {} యొక్క అసలు ధర ₹{:.0f}. మీ మొదటి ఆఫర్ ఏమిటి?",
                "offer_accepted": "అద్భుతం! మనకి ఒక ఒప్పందం కుదిరింది. చివరి ధర ₹{:.0f}.",
                "goodbye": "మీ ఆసక్తికి ధన్యవాదాలు! మీ రోజు అద్భుతంగా గడవాలని కోరుకుంటున్నాను!",
                "discount_applied": "మా ప్రస్తుత పండుగ ఆఫర్ ఆధారంగా, అదనంగా {}% డిస్కౌంట్ వర్తింపజేయబడింది!",
                "loyalty_discount": "నమ్మకమైన కస్టమర్‌గా ఉన్నందుకు ధన్యవాదాలు! మీ లాయల్టీ పాయింట్‌ల కోసం అదనంగా {}% డిస్కౌంట్ వర్తింపజేయబడింది!",
                "current_price": "ఈ {} యొక్క ప్రస్తుత ధర ₹{:.0f}. మీ తదుపరి ఆఫర్ ఏమిటి?",
                "invalid_price": "దయచేసి సరైన ధరను నమోదు చేయండి.",
                "seller_offer_received": "విక్రేత: కస్టమర్ ఆఫర్ స్వీకరించబడింది: ₹{:.0f}",
                "offer_too_low_options": [
                    "ఆ ఆఫర్ చాలా తక్కువగా ఉంది. దయచేసి ఎక్కువ ఆఫర్‌తో మళ్లీ ప్రయత్నించండి.",
                    "మేము దానిని అంగీకరించలేము. మా కనీస ధర మీ ఆఫర్ కంటే ఎక్కువ. దయచేసి మళ్లీ ప్రయత్నించండి.",
                    "మీ ఆఫర్ పరిగణించదగినంత తక్కువగా ఉంది. మీ తదుపరి ధర ఏమిటి?",
                    "క్షమించండి, కానీ అది మాకు ఆమోదయోగ్యం కాని కనీస ధర కంటే తక్కువ. దయచేసి మీ ఆఫర్‌ను పెంచండి."
                ],
                "counter_offer_options": [
                    "మీ ₹{:.0f} ఆఫర్‌కు ధన్యవాదాలు. అది కొంచెం తక్కువగా ఉంది. మధ్యలో ₹{:.0f} వద్ద కలుద్దామా?",
                    "అది ఒక మంచి ప్రారంభం, కానీ మాకు అది సరైనది కాదు. మధ్యలో ₹{:.0f} వద్ద కలుద్దాం.",
                    "మీ ₹{:.0f} ఆఫర్‌ను నేను అభినందిస్తున్నాను. తేడాను విభజిద్దాం. నేను ₹{:.0f} ని అంగీకరించగలను.",
                    "నేను ఆ ధరను అంగీకరించలేను. అయితే, నేను మీకు ₹{:.0f} ప్రతి-ధరను అందించగలను."
                ]
            },
            "hi": {
                "welcome": "नमस्ते! मैं इस सुंदर {} के लिए AI मोलभाव सहायक हूँ। आपकी क्या पेशकश है?",
                "original_price": "इस {} की मूल कीमत ₹{:.0f} है। आपकी पहली पेशकश क्या है?",
                "offer_accepted": "उत्कृष्ट! हमारा सौदा हो गया। अंतिम कीमत ₹{:.0f} है।",
                "goodbye": "आपकी रुचि के लिए धन्यवाद! आपका दिन शुभ हो!",
                "discount_applied": "हमारे चल रहे त्योहार की पेशकश के आधार पर, एक अतिरिक्त {}% छूट लागू की गई है!",
                "loyalty_discount": "एक वफादार ग्राहक होने के लिए धन्यवाद! आपके लॉयल्टी पॉइंट्स के लिए एक अतिरिक्त {}% छूट लागू की गई है!",
                "current_price": "इस {} की वर्तमान कीमत ₹{:.0f} है। आपकी अगली पेशकश क्या है?",
                "invalid_price": "कृपया एक वैध मूल्य दर्ज करें।",
                "seller_offer_received": "विक्रेता: ग्राहक का प्रस्ताव प्राप्त हुआ: ₹{:.0f}",
                "offer_too_low_options": [
                    "वह पेशकश बहुत कम है। कृपया एक उच्च प्रस्ताव के साथ पुनः प्रयास करें।",
                    "हम इसे स्वीकार नहीं कर सकते। हमारी न्यूनतम कीमत आपके प्रस्ताव से अधिक है। कृपया पुनः प्रयास करें।",
                    "आपका प्रस्ताव विचार करने के लिए बहुत कम है। आपकी अगली कीमत क्या है?",
                    "मुझे खेद है, लेकिन यह हमारी न्यूनतम स्वीकार्य कीमत से कम है। कृपया अपनी पेशकश बढ़ाएँ।"
                ],
                "counter_offer_options": [
                    "आपके ₹{:.0f} के प्रस्ताव के लिए धन्यवाद। वह थोड़ा कम है। बीच में ₹{:.0f} पर मिलने के बारे में क्या विचार है?",
                    "यह एक अच्छी शुरुआत है, लेकिन यह बिल्कुल वैसा नहीं है जैसा हमने सोचा था। आइए बीच में ₹{:.0f} पर मिलते हैं।",
                    "मैं आपके ₹{:.0f} के प्रस्ताव की सराहना करता हूँ। आइए अंतर को आधा करते हैं। मैं ₹{:.0f} स्वीकार कर सकता हूँ।",
                    "मैं उस कीमत को स्वीकार नहीं कर सकता। हालांकि, मैं आपको ₹{:.0f} का प्रति-मूल्य दे सकता हूँ।"
                ]
            },
            "pa": {
                "welcome": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਇਸ ਸੁੰਦਰ {} ਲਈ AI ਸੌਦੇਬਾਜ਼ੀ ਸਹਾਇਕ ਹਾਂ। ਤੁਹਾਡੀ ਪੇਸ਼ਕਸ਼ ਕੀ ਹੈ?",
                "original_price": "ਇਸ {} ਦੀ ਅਸਲ ਕੀਮਤ ₹{:.0f} ਹੈ। ਤੁਹਾਡੀ ਪਹਿਲੀ ਪੇਸ਼ਕਸ਼ ਕੀ ਹੈ?",
                "offer_accepted": "ਬਹੁਤ ਵਧੀਆ! ਸਾਡਾ ਸੌਦਾ ਹੋ ਗਿਆ ਹੈ। ਅੰਤਿਮ ਕੀਮਤ ₹{:.0f} ਹੈ।",
                "goodbye": "ਤੁਹਾਡੀ ਦਿਲਚਸਪੀ ਲਈ ਧੰਨਵਾਦ! ਤੁਹਾਡਾ ਦਿਨ ਸ਼ੁਭ ਹੋਵੇ!",
                "discount_applied": "ਸਾਡੀ ਚੱਲ ਰਹੀ ਤਿਉਹਾਰ ਦੀ ਪੇਸ਼ਕਸ਼ ਦੇ ਅਧਾਰ 'ਤੇ, ਇੱਕ ਵਾਧੂ {}% ਛੂਟ ਲਾਗੂ ਕੀਤੀ ਗਈ ਹੈ!",
                "loyalty_discount": "ਇੱਕ ਵਫ਼ਾਦਾਰ ਗਾਹਕ ਹੋਣ ਲਈ ਤੁਹਾਡਾ ਧੰਨਵਾਦ! ਤੁਹਾਡੇ ਲੌਇਲਟੀ ਪੁਆਇੰਟਸ ਲਈ ਇੱਕ ਵਾਧੂ {}% ਛੂਟ ਲਾਗੂ ਕੀਤੀ ਗਈ ਹੈ!",
                "current_price": "ਇਸ {} ਦੀ ਮੌਜੂਦਾ ਕੀਮਤ ₹{:.0f} ਹੈ। ਤੁਹਾਡੀ ਅਗਲੀ ਪੇਸ਼ਕਸ਼ ਕੀ ਹੈ?",
                "invalid_price": "ਕਿਰਪਾ ਕਰਕੇ ਇੱਕ ਵੈਧ ਕੀਮਤ ਦਰਜ ਕਰੋ।",
                "seller_offer_received": "ਵਿਕਰੇਤਾ: ਗਾਹਕ ਦੀ ਪੇਸ਼ਕਸ਼ ਪ੍ਰਾਪਤ ਹੋਈ: ₹{:.0f}",
                "offer_too_low_options": [
                    "ਉਹ ਪੇਸ਼ਕਸ਼ ਬਹੁਤ ਘੱਟ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਇੱਕ ਉੱਚ ਪੇਸ਼ਕਸ਼ ਨਾਲ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
                    "ਅਸੀਂ ਇਸਨੂੰ ਸਵੀਕਾਰ ਨਹੀਂ ਕਰ ਸਕਦੇ। ਸਾਡੀ ਘੱਟੋ-ਘੱਟ ਕੀਮਤ ਤੁਹਾਡੀ ਪੇਸ਼ਕਸ਼ ਤੋਂ ਵੱਧ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
                    "ਤੁਹਾਡੀ ਪੇਸ਼ਕਸ਼ 'ਤੇ ਵਿਚਾਰ ਕਰਨ ਲਈ ਬਹੁਤ ਘੱਟ ਹੈ। ਤੁਹਾਡੀ ਅਗਲੀ ਕੀਮਤ ਕੀ ਹੈ?",
                    "ਮੈਨੂੰ ਅਫਸੋਸ ਹੈ, ਪਰ ਇਹ ਸਾਡੀ ਸਭ ਤੋਂ ਘੱਟ ਸਵੀਕਾਰਯੋਗ ਕੀਮਤ ਤੋਂ ਘੱਟ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਪੇਸ਼ਕਸ਼ ਵਧਾਓ।"
                ],
                "counter_offer_options": [
                    "ਤੁਹਾਡੀ ₹{:.0f} ਦੀ ਪੇਸ਼ਕਸ਼ ਲਈ ਧੰਨਵਾਦ। ਇਹ ਥੋੜ੍ਹਾ ਘੱਟ ਹੈ। ਵਿਚਕਾਰ ₹{:.0f} 'ਤੇ ਮਿਲਣ ਬਾਰੇ ਕੀ ਖਿਆਲ ਹੈ?",
                    "ਇਹ ਇੱਕ ਚੰਗੀ ਸ਼ੁਰੂਆਤ ਹੈ, ਪਰ ਇਹ ਬਿਲਕੁਲ ਉਹੀ ਨਹੀਂ ਹੈ ਜੋ ਅਸੀਂ ਸੋਚਿਆ ਸੀ। ਆਓ ਵਿਚਕਾਰ ₹{:.0f} 'ਤੇ ਮਿਲਦੇ ਹਾਂ।",
                    "ਮੈਂ ਤੁਹਾਡੀ ₹{:.0f} ਦੀ ਪੇਸ਼ਕਸ਼ ਦੀ ਕਦਰ ਕਰਦਾ ਹਾਂ। ਆਓ ਅੰਤਰ ਨੂੰ ਵੰਡਦੇ ਹਾਂ। ਮੈਂ ₹{:.0f} ਸਵੀਕਾਰ ਕਰ ਸਕਦਾ ਹਾਂ।",
                    "ਮੈਂ ਉਸ ਕੀਮਤ ਨੂੰ ਸਵੀਕਾਰ ਨਹੀਂ ਕਰ ਸਕਦਾ। ਹਾਲਾਂਕਿ, ਮੈਂ ਤੁਹਾਨੂੰ ₹{:.0f} ਦਾ ਇੱਕ ਵਿਕਲਪਕ ਮੁੱਲ ਪੇਸ਼ ਕਰ ਸਕਦਾ ਹਾਂ।"
                ]
            },
            "bn": {
                "welcome": "হ্যালো! আমি এই সুন্দর {} এর জন্য এআই দর কষাকষি সহকারী। আপনার প্রস্তাব কি?",
                "original_price": "এই {} এর আসল দাম ₹{:.0f}। আপনার প্রথম প্রস্তাব কি?",
                "offer_accepted": "চমৎকার! আমাদের একটি চুক্তি হয়েছে। চূড়ান্ত মূল্য ₹{:.0f}।",
                "goodbye": "আপনার আগ্রহের জন্য ধন্যবাদ! আপনার দিনটি চমৎকার হোক!",
                "discount_applied": "আমাদের চলমান উৎসবের প্রস্তাবের উপর ভিত্তি করে, একটি অতিরিক্ত {}% ছাড় প্রয়োগ করা হয়েছে!",
                "loyalty_discount": "একজন বিশ্বস্ত গ্রাহক হওয়ার জন্য আপনাকে ধন্যবাদ! আপনার লয়্যালটি পয়েন্টের জন্য একটি অতিরিক্ত {}% ছাড় প্রয়োগ করা হয়েছে!",
                "current_price": "এই {} এর বর্তমান মূল্য ₹{:.0f}। আপনার পরবর্তী প্রস্তাব কি?",
                "invalid_price": "একটি বৈধ মূল্য লিখুন।",
                "seller_offer_received": "বিক্রেতা: গ্রাহকের প্রস্তাব প্রাপ্ত হয়েছে: ₹{:.0f}",
                "offer_too_low_options": [
                    "এই প্রস্তাবটি খুব কম। অনুগ্রহ করে আরও বেশি দাম প্রস্তাব করে আবার চেষ্টা করুন।",
                    "আমরা এটি গ্রহণ করতে পারি না। আমাদের সর্বনিম্ন মূল্য আপনার প্রস্তাবের চেয়ে বেশি। অনুগ্রহ করে আবার চেষ্টা করুন।",
                    "আপনার প্রস্তাব বিবেচনা করার জন্য খুব কম। আপনার পরবর্তী মূল্য কত?",
                    "আমি দুঃখিত, কিন্তু এটি আমাদের সর্বনিম্ন গ্রহণযোগ্য মূল্যের নিচে। অনুগ্রহ করে আপনার প্রস্তাব বাড়ান।"
                ],
                "counter_offer_options": [
                    "আপনার ₹{:.0f} প্রস্তাবের জন্য ধন্যবাদ। এটি একটু কম। মাঝখানে ₹{:.0f} এ দেখা করার বিষয়ে কি ভাবেন?",
                    "এটি একটি ভাল শুরু, কিন্তু এটি আমরা যা ভেবেছিলাম তার মতো নয়। আসুন মাঝখানে ₹{:.0f} এ দেখা করি।",
                    "আমি আপনার ₹{:.0f} প্রস্তাবের প্রশংসা করি। আসুন পার্থক্যটি ভাগ করি। আমি ₹{:.0f} গ্রহণ করতে পারি।",
                    "আমি সেই মূল্য গ্রহণ করতে পারি না। তবে, আমি আপনাকে ₹{:.0f} এর একটি পাল্টা মূল্য দিতে পারি।"
                ]
            }
        }

    def _translate(self, text, target_language):
        """
        A placeholder function to simulate language translation.
        This translates a given text into the target language.
        """
        return self.translations.get(target_language, self.translations["en"]).get(text, text)

    def _auto_apply_discounts(self, final_price):
        """
        Applies eligible discounts based on various conditions.
        """
        applied_discounts = []
        
        # Simulate a festival offer being active
        if time.localtime().tm_mon == 12: # December, for example
            final_price *= (1 - self.discounts["festival"])
            applied_discounts.append(self._translate("discount_applied", self.customer_language).format(self.discounts["festival"] * 100))
        
        # Simulate checking for loyalty points
        if self.loyalty_points > 50:
            final_price *= (1 - self.discounts["loyalty"])
            applied_discounts.append(self._translate("loyalty_discount", self.customer_language).format(self.discounts["loyalty"] * 100))

        return final_price, applied_discounts

    def handle_offer(self, offer_price):
        """
        Handles a customer's price offer and provides a response.
        
        Args:
            offer_price (float): The price offered by the customer.
        
        Returns:
            str: The chatbot's response text.
        """
        # Check if the offer is equal to or greater than the current asking price
        if offer_price >= self.current_price:
            final_price, applied_discounts = self._auto_apply_discounts(offer_price)
            self.is_accepted = True
            response = self._translate("offer_accepted", self.customer_language).format(final_price)
            if applied_discounts:
                response += "\n" + "\n".join(applied_discounts)
            return response
        
        # If the offer is too low (below the minimum price)
        elif offer_price < self.min_price:
            rejection_options = self.translations.get(self.customer_language, self.translations["en"])["offer_too_low_options"]
            return random.choice(rejection_options)

        # If the offer is between the current price and minimum, provide a counter-offer
        else: # offer_price < self.current_price and offer_price >= self.min_price:
            counter_offer_price = (offer_price + self.current_price) / 2
            self.current_price = counter_offer_price
            counter_offer_options = self.translations.get(self.customer_language, self.translations["en"])["counter_offer_options"]
            selected_response = random.choice(counter_offer_options)
            return selected_response.format(offer_price, self.current_price)

    def start_negotiation(self):
        """
        Starts the bargaining conversation loop.
        """
        print("Bargaining Chatbot Initializing...")
        time.sleep(1)
        
        # Show original price and start the bargaining
        print(self._translate("original_price", self.customer_language).format(self.product_name, self.ideal_price))

        while not self.is_accepted:
            try:
                user_input = input(f"({self.customer_language}) > ")
                offer = float(user_input.strip('₹'))
                
                # Show the offer to the seller in their chosen language
                print(self._translate("seller_offer_received", self.seller_language).format(offer))
                
                response = self.handle_offer(offer)
                print(f"Chatbot > {response}")
                
                if self.is_accepted:
                    break
            except ValueError:
                print(f"Chatbot > {self._translate('invalid_price', self.customer_language)}")

        print(self._translate("goodbye", self.customer_language))

if __name__ == "__main__":
    
    # Language Selection Section
    language_map = {
        "english": "en",
        "telugu": "te",
        "hindi": "hi",
        "punjabi": "pa",
        "bengali": "bn"
    }
    available_languages = list(language_map.keys())
    
    seller_language = ""
    while seller_language not in available_languages:
        seller_language = input(f"Seller, please choose your language ({', '.join(available_languages)}): ").strip().lower()

    customer_language = ""
    while customer_language not in available_languages:
        customer_language = input(f"Customer, please choose your language ({', '.join(available_languages)}): ").strip().lower()

    print("--------------------------------------------------")

    # Example usage:
    # In a real app, this data would come from a database.
    product_data = {
        "name": "Hand-carved wooden bowl",
        "ideal_price": 5000.00,
        "min_price": 3500.00
    }

    chatbot = BargainingChatbot(
        product_name=product_data["name"],
        ideal_price=product_data["ideal_price"],
        min_price=product_data["min_price"],
        customer_language=language_map[customer_language],
        seller_language=language_map[seller_language]
    )

    # You can manually set loyalty points to test that logic
    # chatbot.loyalty_points = 100

    chatbot.start_negotiation()
    input("Press Enter to exit...")
