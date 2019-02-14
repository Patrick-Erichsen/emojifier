package com.hackathon.emojifier.services;

import com.github.jfasttext.JFastText;
import com.hackathon.emojifier.Utilities.ClassifierConfiguration;
import com.hackathon.emojifier.Utilities.Constants;
import java.util.HashMap;
import java.util.Map;
import org.springframework.stereotype.Component;

@Component("classifier")
public class Classifier {

    private JFastText jFastText = new JFastText();

    Classifier() {
        log("I'm being created!");
        trainData();
    }

    private void trainData() {
        log("Beginning to train data");

        jFastText.runCmd(new String[] {
            "supervised",
            "-input", Constants.PATH_TO_LABELED_DATA,
            "-output", Constants.PATH_TO_OUTPUT_MODEL,
            "-epoch" , ClassifierConfiguration.EPOCHS,
            "-lr", ClassifierConfiguration.LEARNING_RATE
        });

        jFastText.loadModel(String.format("%s.bin", Constants.PATH_TO_OUTPUT_MODEL));
    }

    /*
        UTILITY METHODS
     */
    private static void log(final String logMessage) {
        System.out.println(logMessage);
    }

    public String makePrediction(final String input) {
        // Do label prediction
        JFastText.ProbLabel probLabel = jFastText.predictProba("wow");
        String prediction = String.format("\nThe label of '%s' is '%s' with probability %f\n",
            input, probLabel.label, Math.exp(probLabel.logProb));

        return prediction;
    }

    public Map<String, Object> guessLabel(final String input) {

        final String KEY_LABEL = "label";
        final String KEY_CONFIDENCE = "confidence";

        Map<String, Object> guessDictionary = new HashMap<String, Object>() {
            {
                put(KEY_LABEL, "n/a");
                put(KEY_CONFIDENCE, Float.valueOf(0.0f));
            }
        };

        JFastText.ProbLabel probLabel = jFastText.predictProba(input);

        if (probLabel != null) {

            guessDictionary.put(KEY_LABEL, probLabel.label);
            guessDictionary.put(KEY_CONFIDENCE, probLabel.logProb);
        }

        return guessDictionary;
    }
}
