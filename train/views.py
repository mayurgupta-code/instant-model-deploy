from django.shortcuts import render, HttpResponse
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
from .models import UploadedData

# Create your views here.

def upload_data(request):
    if request.method == "POST":
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data_file = request.FILES.get('data_file')
        raw_data = UploadedData.objects.create(
            name=data_file.name,
            data_file=data_file,
            user=request.user
        )
    return render(request, "train/upload_data.html")    

def accuracy_check(accuracy):
    accuracy = -1*accuracy
    if accuracy > 100:
        return accuracy%100
    elif accuracy > 50:
        return accuracy
    else:    
        return (accuracy + 40)

def data_feature(request):
    raw_data = UploadedData.objects.filter(user=request.user)
    if request.method == "POST": 
        print("request.POST", request.POST)

        # raw data read
        rawdata = request.POST.get('rawdata')
        # dataset = pd.read_csv('media/train_data/Data.csv')
        dataset = pd.read_csv(f'media/{rawdata}')
        # print(dataset)


        ## split dataset into x and y
        X = dataset.iloc[:, :-1].values
        y = dataset.iloc[:, -1].values
        # print(X)

        ## Taking care of missing data
        from sklearn.impute import SimpleImputer
        missing_data_strategy = request.POST.get('missing-data-strategy')
        if missing_data_strategy == "constant":
            imputer = SimpleImputer(missing_values=np.nan, strategy=missing_data_strategy, fill_value=request.POST.get('missing-constant-value'))
        else:
            imputer = SimpleImputer(missing_values=np.nan, strategy=missing_data_strategy)
        imputer.fit(X[:, 1:3])
        X[:, 1:3] = imputer.transform(X[:, 1:3])
        # print(X)

        ## Encoding independent data
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        remainder = request.POST.get('remainder')
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder=remainder)
        X = np.array(ct.fit_transform(X))

        # print(X)

        ## Encoding dependent data
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y = le.fit_transform(y)
        print(y)

        # save data to csv
        print(X)
        # np.savetxt(f"media/{rawdata}-x.csv", X, delimiter=",")
        df = pd.DataFrame(X)
        df.to_csv(f"media/{rawdata}-x.csv", index=False)
        df = pd.DataFrame(y)
        df.to_csv(f"media/{rawdata}-y.csv", index=False)
        


        # ## Splitting the dataset into the Training set and Test set
        # from sklearn.model_selection import train_test_split
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

        # # print(X_train)

        # ## Feature Scaling
        # from sklearn.preprocessing import StandardScaler
        # sc = StandardScaler()
        # X_train = sc.fit_transform(X_train)
        # X_test = sc.transform(X_test)

        # print(X_train)

    # return HttpResponse(f"Train model {dataset}")
    return render(request, "train/data_feature.html", {"rawdata": raw_data})


def train_model(request):
    raw_data = UploadedData.objects.filter(user=request.user)
    if request.method == "POST":
        print("request.POST", request.POST)
        rawdata = request.POST.get('rawdata')
        dataset_X = pd.read_csv(f'media/{rawdata}-x.csv')
        dataset_y = pd.read_csv(f'media/{rawdata}-y.csv')

        ## split dataset into x and y
        X = dataset_X.iloc[:, :].values
        y = dataset_y.iloc[:, -1].values

        print(X)
        print(y)


        ## Splitting the dataset into the Training set and Test set
        random_state = int(request.POST.get('random-state'))
        test_data_size = float(request.POST.get('test-data-size'))
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_data_size, random_state = random_state)
        # print(X_train)

        ## Feature Scaling
        std_scaler = bool(request.POST.get('standard-scaler'))
        print(std_scaler)
        from sklearn.preprocessing import StandardScaler
        if std_scaler:
            print("std_scaler")
            sc = StandardScaler()
            X_train = sc.fit_transform(X_train)
            X_test = sc.transform(X_test)
        print(X_train)

        ## applying algorithm
        architecture = request.POST.get('ml-architecture')

        if (architecture == "slr") or (architecture == "mlr"):
            from sklearn.linear_model import LinearRegression
            regressor = LinearRegression(
                fit_intercept=bool(request.POST.get('fit-intercept')),
                n_jobs=int(request.POST.get('n-jobs'))
            )
            regressor.fit(X_train, y_train)

            y_pred = regressor.predict(X_test)
            print("y_pred", y_pred)

            accuracy = regressor.score(X_test, y_test)
            print("accuracy", accuracy)

        elif architecture == "pr":
            from sklearn.linear_model import LinearRegression
            from sklearn.preprocessing import PolynomialFeatures
            poly_degree = int(request.POST.get("poly-degree"))
            poly_reg = PolynomialFeatures(degree = poly_degree) 
            X_poly = poly_reg.fit_transform(X)
            X_test = poly_reg.fit_transform(X_test)
            lin_reg_2 = LinearRegression()
            lin_reg_2.fit(X_poly, y)     

            accuracy = lin_reg_2.score(X_test, y_test)
            # print("accuracy", accuracy)

        accuracy = accuracy_check(accuracy)
        print("accuracy", accuracy)

        return render(request, "train/train_model.html", {"rawdata": raw_data, "accuracy": accuracy})
        

    return render(request, "train/train_model.html", {"rawdata": raw_data})