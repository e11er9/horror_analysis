Figure 3.1 - Residual Plot For Linear Regression

This residual plot shows that linear regression has a strong pattern in its errors and struggles the most with both low and high revenue movies

Figure 3.2 - Residual Plot For Random Forest

The random forest plot is more spread out, and the residuals look more random for more of the predictions. For movies with a higher predicted revenue the model seems to perform well, but has trouble with movies that have a low predicted revenue

Figure 3.3 - Residual Plot For Gradient Boosting

The gradient boosting plot looks similar to random forest. Most residuals are centered around zero and look random, especially for medium and high predicted revenue. The same diagonal line appears for low revenue movies, showing that the model still struggles most with films that earned almost nothing.


Figure 4.1 - Top 10 Important Features for Gradient Boosting

This figure shows the top 10 features that the gradient boosting model used to predict log revenue for horror movies. IMDb votes and log versions of votes and budget are much more important than the other features, which means the model relies mainly on audience engagement and the scale of a movie's production when making predictions. This matters because it supports the idea that how many people rate a movie and how much money is put into it are the strongest drivers of revenue 


Figure 4.2 - Model Performance Comparison Using R² on Test Set

This bar chart compares how well the three models predict log revenue on the test data. Random Forest and Gradient Boosting are both around 0.74 while Linear Regression is around 0.69. This matters because it shows that tree based models capture more complex patterns in movie revenue than a linear model


Figure 4.3 - Actual vs. Predicted Log Revenue For Gradient Boosting

This scatter plot shows how close the Gradient Boosting predictions are to the actual log revenue values. ​​Points near the dashed line represent accurate predictions and points far above or below represent larger errors. The figure matters because it reveals that the model performs better for higher revenue movies and struggles more with low revenue films. It also more clearly shows that I missed some zeros in cleaning.
