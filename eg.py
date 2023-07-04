import matplotlib.pyplot as plt

# Test files and their respective number of tests
results = {
    'play_scorer_exceptions_test.py': 6,
    'play_scorer_test.py': 41,
    'show_scorer__impossible_score_test.py': 1000,
    'show_scorer_exceptions_test.py': 3,
    'show_scorer_test.py': 48
}

# Data to plot
labels = results.keys()
sizes = results.values()

# Plot
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Pytest Results')
plt.legend(loc='upper left')
plt.show()

