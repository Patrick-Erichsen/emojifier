package com.hackathon.emojifier;

import com.github.jfasttext.JFastText;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import com.hackathon.emojifier.services.Classifier;


@RestController
public class MainController {

    @Autowired
    private Classifier classifier;


    @GetMapping("hello")
    public String sayHello(@RequestParam("search_term") String searchTerm) {

        return classifier.makePrediction(searchTerm);
    }

    @PostMapping("emojifyMap")
    public Map<String, Object> emojifyMap(@RequestBody List<String> inputs) {

        Map<String, Object> guesses = new HashMap<>();

        if (inputs == null || inputs.size() == 0) {
            return guesses;
        }


        for(String input : inputs) {

            final Map<String, Object> guessedValues = classifier.guessLabel(input);

            guesses.put(input, guessedValues);
        }

        return guesses;
    }
}
