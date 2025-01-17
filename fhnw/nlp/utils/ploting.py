
# see https://stackoverflow.com/a/57013458
def plot_grid_search_results(gs, filename=None):
    """
    Params: 
        gs: A trained GridSearchCV object.
    """
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    ## Results from grid search
    results = gs.cv_results_
    means_test = results['mean_test_score']
    stds_test = results['std_test_score']
    means_train = results['mean_train_score']
    stds_train = results['std_train_score']

    params=gs.param_grid
    ## Getting indexes of values per hyper-parameter
    masks=[]
    masks_names= list(gs.best_params_.keys())
    masks_names_print = [xi for xi in gs.best_params_.keys() if len(params[xi]) > 1]
    for p_k, p_v in gs.best_params_.items():
        masks.append([xi == p_v for xi in results['param_'+p_k].data])

    ## Ploting results
    fig, ax = plt.subplots(1,len(masks_names_print),sharex='none',sharey='all',figsize=(20,5),squeeze=False)
    ax = ax.flatten()
    fig.suptitle('Score per parameter')
    fig.text(0.04, 0.5, 'MEAN SCORE', va='center', rotation='vertical')
    pram_preformace_in_best = {}
    j = 0
    for i, p in enumerate(masks_names):
        if p in masks_names_print:
            m = np.stack(masks[:i] + masks[i+1:])
            pram_preformace_in_best
            best_parms_mask = m.all(axis=0)
            best_index = np.where(best_parms_mask)[0]
            #x = np.array(params[p])
            x = [str(item) for item in params[p]]
            y_1 = np.array(means_test[best_index])
            e_1 = np.array(stds_test[best_index])
            y_2 = np.array(means_train[best_index])
            e_2 = np.array(stds_train[best_index])
            ax[j].errorbar(x, y_1, e_1, linestyle='--', marker='o', label='test')
            ax[j].errorbar(x, y_2, e_2, linestyle='-', marker='^',label='train' )
            ax[j].set_xlabel(p.upper())
            j += 1

    plt.legend()
    
    if filename is not None:
        plt.savefig(filename, dpi=300)
    else: 
        plt.show()

def plot_confusion_matrix(y_true, y_pred, title='', percentage=True, filename=None):
    """Plots or stores the confusion matrix 

    Parameters: 
        y_true: list/array
            The true labels
        y_pred: list/array
            The predicted labels
        title: str
            The title of the plot
        percentage: bool 
            Defines if percentage or number of samples should be printed for each category
        filename: str
            The path and name of the file to save the confusion matrix (will not be plotted to the screen if set)
    """
    
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix
    
    classes = list(set(list(y_true) + list(y_pred)))
    classes.sort()

    cmm = confusion_matrix(y_true, y_pred)

    print('Set Population: {}'.format(cmm.sum()))
    print('Accuracy: {:.4f}'.format(float(cmm.trace()) / cmm.sum()))

    plt.figure(figsize=(10, 8))
    plt.imshow(np.flip(cmm / cmm.sum(), 0), interpolation='nearest', cmap='Blues')
    plt.title(title)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.colorbar()

    plt.ylim(-0.5, len(classes)-0.5)

    if classes is not None:
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45, size='x-large')
        plt.yticks(np.flip(tick_marks), classes, size='x-large')

    cmm_flip = np.flip(cmm, 0)
    for y in range(cmm.shape[0]):
        for x in range(cmm.shape[1]):
            if cmm_flip[y, x] > 0:
                if percentage:
                    plt.text(x, y, '%.3f' % ((cmm_flip[y, x] / cmm.sum())),
                         horizontalalignment='center',
                         verticalalignment='center')
                else:
                    plt.text(x, y, '%.0i' % cmm_flip[y, x],
                         horizontalalignment='center',
                         verticalalignment='center')
    
    if filename is not None:
        plt.savefig(filename, dpi=300)
    else: 
        plt.show()
        

def create_word_cloud(df, label, field="token_lemma"):
    """Creates a wordcloud of a column of text

    Parameters
    ----------
    df : dataframe
        The dataframe
    field : str
        The column name to read from (default is token_lemma)
    """
        
    import matplotlib.pyplot as plt
    from collections import Counter
    from wordcloud import WordCloud
    
    counter = Counter()
    # see https://stackoverflow.com/a/17071908
    _ = df["token_lemma"].apply(counter.update)
    
    print(label, "- with", len(counter.keys()), "number of words.")

    wc = WordCloud(background_color="white", max_words=1000)
    wc.generate_from_frequencies(counter)

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
    
def plot_ngram_counts(counter, n_most_common, title="Term frequencies"):
    """Plots the n-gram counts

    Parameters
    ----------
    counter : Counter
        The counter of the n-grams
    n_most_common : int
        The n most common n-grams to plog
    title : str
        The title of the plot
    """
    
    import matplotlib.pyplot as plt
        
    y = [count for tag, count in counter.most_common(n_most_common)]
    x = [tag for tag, count in counter.most_common(n_most_common)]

    plt.bar(x, y)
    plt.title(title)
    plt.ylabel("Frequency")
    #plt.yscale('log') # set log scale for y-axis
    plt.xticks(rotation=90)
    for i, (tag, count) in enumerate(counter.most_common(n_most_common)):
        plt.text(i, count, f' {count} ', rotation=90, ha='center', va='top' if i < 10 else 'bottom', color='white' if i < 10 else 'black')
    plt.xlim(-0.6, len(x)-0.4) # set tighter x lims
    plt.tight_layout() # change the whitespace such that all labels fit nicely
    plt.show()
    
import matplotlib.pyplot as plt 


def plot_feature_importance(classifier, feature_names, top_features=20):
    """Plot the feature importance of the top n features of a LinearSVC

    Parameters
    ----------
    classifier : LinearSVC
        The classifier
    feature_names : iterable
        The name of the features
    top_features : int
        The top n features to plog
    """
    
    import matplotlib.pyplot as plt 
        
    coefs = classifier.coef_
    n_coefs = len(coefs)
    
    for i in range(n_coefs):
        label = classifier.classes_[i] + ("" if n_coefs >= len(classifier.classes_) else "/"+classifier.classes_[i + 1])
        coef = coefs[i,]
    
        top_positive_coefficients = np.argsort(coef)[-top_features:]
        top_negative_coefficients = np.argsort(coef)[:top_features]
        top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
 
        # create plot
        plt.figure(figsize=(15, 5))
        colors = ["red" if c < 0 else "green" for c in coef[top_coefficients]]
        plt.bar(np.arange(2 * top_features), coef[top_coefficients], color=colors)
        feature_names = np.array(feature_names)
        plt.xticks(np.arange(1, 1 + 2 * top_features), feature_names[top_coefficients], rotation=60, ha="right")
        plt.title(label)
        plt.show()


def plot_history(history, filename=None):
    """Plots or stores the history of an optimization run

    Parameters: 
        history: history
            The history to plot
        filename: str
            The path and name of the file to save the confusion matrix (will not be plotted to the screen if set)
    """
    
    import matplotlib.pyplot as plt
        
    plt.title('Accuracy')
    plt.plot(history.history['accuracy'], label='train')
    plt.plot(history.history['val_accuracy'], label='test')
    plt.legend()
    plt.show()

    plt.title('Loss')
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    
    if filename is not None:
        plt.savefig(filename, dpi=300)
    else: 
        plt.show()


def report_classification_results(params, data, model):
    """Reports all classification results

    Parameters: 
        params: dict
            The dictionary containing the parameters
        data: dataframe
            The data
        model: model
            The keras model
    """
    
    import os
    from sklearn.metrics import classification_report
    from fhnw.nlp.utils.params import predict_classification
    
    verbose = params.get("verbose", False)
    path = params.get("model_path")

    y, y_pred, y_pred_prob = predict_classification(params, data, model)
    
    if path is not None:
        path_confusion_matrix = os.path.join(path, "confusion_matrix.png")
        plot_confusion_matrix(y, y_pred, filename=path_confusion_matrix)
    if verbose:
        plot_confusion_matrix(y, y_pred)
        
    if path is not None:
        path_classification_report = os.path.join(path, "classification_report.csv")
        report = classification_report(y, y_pred, output_dict=True)
        report = pandas.DataFrame(report).transpose()
        report.to_csv(path_classification_report)
    if verbose:
        report = classification_report(y, y_pred)
        print(report)
