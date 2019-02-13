package com.hackathon.emojifier;

import Utilities.Constants;
import com.github.jfasttext.JFastText;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class EmojifierApplication {

	public static void main(String[] args) {

		SpringApplication.run(EmojifierApplication.class, args);

		JFastText jft = new JFastText();

		// Train supervised model
		jft.runCmd(new String[] {
			"supervised",
			"-input", Constants.PATH_TO_LABELED_DATA,
			"-output", Constants.PATH_TO_OUTPUT_MODEL
		});

		String text = "What is the most popular sport in the US ?";
		JFastText.ProbLabel probLabel = jft.predictProba(text);
		System.out.printf("\nThe label of '%s' is '%s' with probability %f\n",
			text, probLabel.label, Math.exp(probLabel.logProb));
	}

}



