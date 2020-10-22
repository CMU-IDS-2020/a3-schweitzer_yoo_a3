# Project name

![A screenshot of macro view. Could be a GIF.](macroViewA3.jpg)
![A screenshot of individual view. Could be a GIF.](individualViewA3.jpg)

TODO: Short abstract describing the main goals and how you achieved them.

Restaurants - there's a lot to learn about them.  from their ratings, and their review trends. Whether you're someone who likes food, a business owner, or a city planner -- restaurant ratings, characteristics, and over-time data projection offer a great deal of insight. \\This web-app allows users to view two tabs which illuminate this data, configured from Yelp business and review data. Each tab allows users to focus in on a high-level look at city review trends or low-level restaurant-specific infomration. Viewports can be used individually to narrow in on high or low level specific questions, or used together for in depth analysis of overtime trends and projections.

## Project Goals

TODO: **A clear description of the goals of your project.** Describe the question that you are enabling a user to answer. The question should be compelling and the solution should be focused on helping users achieve their goals. 

Our project goals are twofold. We want to provide a tool for both a higher-level and lower-level look at restaurant data. For a business owner or city planner, the first question **(Q1)** is 'how have prefernce sentiment (negative, positive, or neutral) changed overtime and how do these vary between cities?' For a general user, the second question **(Q2)** is 'how can a restaurant search be configured to an in individual's taste and preferences?'

## Design

TODO: **A rationale for your design decisions.** How did you choose your particular visual encodings and interaction techniques? What alternatives did you consider and how did you arrive at your ultimate choices?

**TAB 1**: Macro-City View\
To address **Q1**, we created a viewport allowing a user to view four maps. Maps show restaurant data for Pittsburgh, Montreal, Cleveland, and Toronto. Users can specify a range of stars (1 to 5) with which to filter the data. Maps update to show all restaurants within that star range. A graph below shows how negative, positive, and neutral preference has changed overtime. Users can select select between three buttons ('Negative,' 'Positive,' and 'Neutral') to specify a the sentement of reviews and ratings. The chart updates, colorizing the degree of negativity/positivity/neutrality over each year of submitted reviews to reflect the strength of sentiment. The size of each circle on the graph remains the same and showcases the total number or reviews submitted over time for each. In this view users cannot see the specific data of each city to reduce the over-saturation of information and keep the focus around restaurant sentiment.

**TAB 2**: Individual View\
**Q2** is addressed in a second view port. The visuals here focus in on just one city at a time, allowing users to zero in on more detailed city data without being overwhelmed by information. **< Clay feel free to add specific details here >**

## Development

TODO: **An overview of your development process.** Describe how the work was split among the team members. Include a commentary on the development process, including answers to the following questions: Roughly how much time did you spend developing your application (in people-hours)? What aspects took the most time?

The development process developed within several stages articulated below. Total development time took roughly 92 hours total **< Not exactly sure how much time I put in, but we've met almost every day since last week Saturday = 7hrs x 2 = 14hrs. Spent most of the day each Saturday and Sunday = 16hrs x 2 = 32hrs. Plus initial brainstorming and development time = 8hrs x 2 = 16hrs. And then the development process now, maybe 5ish hrs each day Mon, Tues, Wed, and today? So that'd be (5hrs x 3days) x 2 = 30hrs. In total that'd be 92hrs. Sound about right to you Clay? >**. Figuring out Streamlit, between understanding its processing power, speed, abilities, configuration, and ability to interface with Altair, took the most time at maybe 50%. Debugging came in second for time consumption at around 30%, with the integration process taking maybe 20%. \

**Planning & Testing Options**\
The development process begain in the planning phase in which we considered our interests, questions, and possible topics. These included the following: \

Space Focus: Exoplanet or solar-system data were the fist considerations. We investigated the datasets available and the existing libraries that could help our development. Datasets on exoplanets were available, but because not all data properties were available consistently and no substantial libraries exist for space-specific data, we determined this was not the right path. We estimated the manual processes we would need to perform would overpower our visuaization and machine learning focus with streamlit. Lydia investigated datasets. We both investigated space libraries.\

Art Focus: Next, we considered the option of an art-focussed project. We decided to combine solar system data into this project idea. NASA JPL released a poster series entitled "Exoplanet Travel Bureau." This poster series consists of human-drawn renderings of the worlds that humans could encounter at a figurative level on planets outside of our solar system. Posters show terrain colored by a red sun, or multiple planets in the sky all correlating to the data behind each exoplanet but artistically rendered to transport a viewer to the exoplanet realm. Our plan was to use a machine learning method to transform classically historic paintings using the visual characteristics of planets in our solar system. However, the machine learning process took too long to load on Streamlit, so we moved on. Clay implemented the machine learning to test on Streamlit and Lydia organized planet images and designed interactivity methods.\

We both met often and discussed throughout this process testing out each option thoroughly.\

**Topic Selection & Intermediate Steps**\
Yelp Focus: This focus, our ultimate choice, was a dataset easily structured and provided detailed characteristics about businesses and reviews. We figured we could use this well documented and organized data to build powerful visuals dedicated to spacific user goals.\

Intermediate steps involved designing an interface, parsing and organizing data, and figuring out the Streamlit development platform. Clay parsed and organized the data, Lydia developed intial sketches of visualization interface, and we both investigated the Streamlit visualization platform.\

**< Lydia to insert screenshot of interface design >**\

**Individual Development**\
Now we defined our individual development. Clay focussed on the individual viewport and Lydia focussed on the macro scale view port. We both met frequently to discuss progress, ideas, and direction.\

**Combination & Conclusion**\
The final process involved combining our code. We both pushed our code to the Github repository and Clay integrated the code. Lydia wrote the writeup. Throughout this process, we met frequently to test the integration, and discuss design changes.
