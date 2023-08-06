# automate_LinearRegression

- ### This package is specific to build a Linear Regeression model on the dataset passed as the parameter with its features as well as label to be regressed against. And as such, it is presumed that the analysis and the feature engineering has already been done on the dataset.
    
- ### This package will standardize the data via StandardScaler() so that all features can be on the same scale and obviously so that the model optimization could increase.

- ### Accuracy of the model built by this package is computed using `adjusted R-squared` metric.

- ### User will also have the flexibility of building the model with regularization modes viz. `Lasso (L1`, `Ridge (L2)` and `ElasticNet` and to compare their accuracies accordingly.

## An Example of How to use:


```python
from automate_LinearRegression import automate_linReg
import pandas as pd
import seaborn as sns

# loading a famous 'Iris' dataset from the seaborn module
df = sns.load_dataset("iris")
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sepal_length</th>
      <th>sepal_width</th>
      <th>petal_length</th>
      <th>petal_width</th>
      <th>species</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5.1</td>
      <td>3.5</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>setosa</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4.9</td>
      <td>3.0</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>setosa</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4.7</td>
      <td>3.2</td>
      <td>1.3</td>
      <td>0.2</td>
      <td>setosa</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4.6</td>
      <td>3.1</td>
      <td>1.5</td>
      <td>0.2</td>
      <td>setosa</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5.0</td>
      <td>3.6</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>setosa</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Assuming `sepal_width` is our label

features = df.drop(columns=['sepal_width', 'species'])
label = df['sepal_width']
```


```python
features.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sepal_length</th>
      <th>petal_length</th>
      <th>petal_width</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5.1</td>
      <td>1.4</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4.9</td>
      <td>1.4</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4.7</td>
      <td>1.3</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4.6</td>
      <td>1.5</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5.0</td>
      <td>1.4</td>
      <td>0.2</td>
    </tr>
  </tbody>
</table>
</div>




```python
label.head()
```




    0    3.5
    1    3.0
    2    3.2
    3    3.1
    4    3.6
    Name: sepal_width, dtype: float64




```python
# buidling a linear model

model = automate_linReg(dataframe=df, features=features, label=label)
model.split(testSize=0.2, random_state=1000)
model.build()
```

    INFO 2022-10-22 18:57:26,717 logger activated!
    INFO 2022-10-22 18:57:26,722 Model building initiates..
    INFO 2022-10-22 18:57:26,731 data split is done successfully!
    INFO 2022-10-22 18:57:26,733 readying the model...
    INFO 2022-10-22 18:57:26,739 Model executed succesfully!
    


```python
# Having a look at the training score 

model.accuracy(test_score=False)
```

    INFO 2022-10-22 18:57:26,763 The Regression model appears to be 53.34250683053611% accurate.
    
    53.343




```python
# Accuracy on the test dataset

model.accuracy()
```

    INFO 2022-10-22 18:57:26,779 The Regression model appears to be 49.19831544294634% accurate.
    
    49.198




```python
# Saving model in your local system

model.save(fileName='regression_model')
```

    INFO 2022-10-22 18:57:26,795 The Regression model is saved at D:\ sucessfully!
    

### Let's put some regularization on the top of our model:


```python
# building the model with ElasticNet regularization

model.buildLasso()
```

    INFO 2022-10-22 18:57:26,997 readying the L1 Model...
    INFO 2022-10-22 18:57:27,000 L1 Model executed!
    


```python
# training score

model.accuracy(mode='L1', test_score=False)
```

    INFO 2022-10-22 18:57:27,018 The L1 model appears to be 53.317792187590655% accurate.
   
    53.318




```python
# test score

model.accuracy(mode='L1')
```

    INFO 2022-10-22 18:57:27,051 The L1 model appears to be 49.1579197226467% accurate.
   
    49.158



### Note: Do not mind the accuracies, this dataset is just taken for the sake of an example.
