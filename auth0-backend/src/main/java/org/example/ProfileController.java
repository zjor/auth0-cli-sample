package org.example;

import org.example.auth.JwtAuth;
import org.springframework.security.core.annotation.AuthenticationPrincipal;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProfileController {

    @GetMapping("/profile")
    public Object profile(@AuthenticationPrincipal JwtAuth auth) {
        return auth;
    }
}
