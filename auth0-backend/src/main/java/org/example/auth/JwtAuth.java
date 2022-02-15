package org.example.auth;

import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

import java.util.Date;
import java.util.List;

@Builder
@Getter
@ToString
public class JwtAuth {

    private String subject;
    private List<String> scopes;
    private Date expiresAt;

}
