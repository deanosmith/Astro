# In the body of the 'if __name__ == "__main__":' section
# after the code from the solution...

def placeholder();
    # To verify the claim that most things > redshift ~0.4 are
    # QSOs check the plot of redshifts vs normalized distribution
    # for galaxies and for QSOs.
    n_galaxies = len(galaxies['redshift'])
    n_qsos = len(qsos['redshift'])
    # Weights array: Each element will be 1 / (total elements)
    # for galaxies and QSOs respectively, so that the weight of
    # every element adds up to 1, thus normalizing them.
    g_weights = np.ones(n_galaxies) / float(n_galaxies)
    q_weights = np.ones(n_qsos) / float(n_qsos)
    # The width of each bin for the histogram, make it thin!
    binwidth = 0.01
    # Histogram for galaxies and QSOs.
    # This is to create an individual figure, after a new one
    # is called all plt.something calls will be done on the
    # latest figure.
    figure_1 = plt.figure(1)
    # The bins arg determine the range (min, max) and the width.
    qsos_hist = plt.hist(qsos['redshift'], label='QSOs', weights=q_weights, bins=np.arange(min(qsos['redshift']), max(qsos['redshift']) + binwidth, binwidth))
    galaxies_hist = plt.hist(galaxies['redshift'], label='Galaxies', weights=g_weights, bins=np.arange(min(galaxies['redshift']), max(galaxies['redshift']) + binwidth, binwidth))

    # Set the limit to cut off really very redshifted QSOs.
    plt.xlim(0, 3)
    plt.xlabel('Redshift')
    plt.ylabel('Normalized Distribution')
    plt.legend()

    # Now see that also in the measured vs predicted redshifts
    # there's also a grouping of galaxies in < redshift ~0.4
    # values with very good accuracy and from that point on a
    # lot of QSOs with less accurate fitting.
    galaxies_preds = cross_validate_predictions_data(galaxies)
    qsos_preds = cross_validate_predictions_data(qsos)

    figure_2 = plt.figure(2)
    qsos_plot = plt.scatter(qsos['redshift'], qsos_preds, s=0.4, label='QSOs')
    galaxies_plot = plt.scatter(galaxies['redshift'], galaxies_preds, s=0.4, label='Galaxies')
    # Put the limits to cut really far away outliers.
    plt.xlim(0, 3)
    plt.ylim(0, 3)
    plt.xlabel('Measured Redshift')
    plt.ylabel('Predicted Redshift')
    plt.legend()

    # Call this only at the very end so that both figures will 
    # displayed!
    plt.show()


def cross_validate_predictions_data(data):
    # Generate the features and targets.
    features, targets = get_features_targets(data)
    # Initialize model with a maximum depth of 19 which was
    # found to be approximately our sort-of overfitting limit.
    dtr = DecisionTreeRegressor(max_depth=19)
    
    # Return the redshift predictions for this dataset.
    return cross_validate_predictions(dtr, features, targets, 10)