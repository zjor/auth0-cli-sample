package org.example.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.swagger.annotations.ApiOperation;
import kong.unirest.HttpResponse;
import kong.unirest.JsonNode;
import kong.unirest.MimeTypes;
import kong.unirest.Unirest;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.example.auth.JwtAuth;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

import static org.example.auth.JwtTokenFilter.BEARER_PREFIX;

@Slf4j
@RestController("api")
public class ProfileController {

    @Value("${auth0.tenantUrl}")
    private String baseUrl;

    @ApiOperation("Returns JWT token information")
    @GetMapping("token")
    public JwtAuth getToken(@AuthenticationPrincipal JwtAuth auth) {
        return auth;
    }

    @SneakyThrows
    @ApiOperation("Gets profile data from Auth0")
    @GetMapping("profile")
    public Object getProfile(@RequestHeader(HttpHeaders.AUTHORIZATION) String authorization) {
        if (!authorization.startsWith(BEARER_PREFIX)) {
            authorization = BEARER_PREFIX + authorization;
        }

        HttpResponse<JsonNode> response = Unirest.get(baseUrl + "userinfo")
                .header(HttpHeaders.AUTHORIZATION, authorization)
                .header(HttpHeaders.CONTENT_TYPE, MimeTypes.JSON).asJson();

        return new ObjectMapper().readValue(response.getBody().toString(), Map.class);
    }
}
